
import streamlit as st

from app.rag.query import Rag


st.set_page_config(
    page_title="College Helpdesk Bot",
    page_icon="NO NEED",
    layout="centered",
)

st.title("College Helpdesk Bot")
st.caption("Your assistant for college academics, admissions, administration, and campus facilities.")

st.info(
    "Answers are generated from the available college documents. "
    "Always verify time-sensitive information with official sources."
)


@st.cache_resource
def load_rag_pipeline():
    return Rag()


try:
    rag_pipeline = load_rag_pipeline()
except Exception as error:
    st.error(f"Could not initialize the helpdesk: {error}")
    st.stop()


if "messages" not in st.session_state:
    st.session_state.messages = []


def display_sources(sources):
    if not sources:
        st.caption("No relevant sources were retrieved.")
        return

    with st.expander(f"Retrieved sources ({len(sources)})"):
        for index, source in enumerate(sources, start=1):
            metadata = source.get("metadata") or {}

            source_name = metadata.get(
                "source", "College document"
            )
            page_number = metadata.get("page_number")

            st.markdown(f"**Source {index}: {source_name}**")

            if page_number is not None:
                st.caption(f"PDF page: {page_number}")

            st.caption(
                f"Relevance distance: "
                f"{source.get('distance', 'N/A')}"
            )

            source_text = source.get("text", "")
            if source_text:
                with st.container(border=True):
                    st.text(source_text)

            if index < len(sources):
                st.divider()


# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            display_sources(message.get("sources", []))


# Accept a new question.
question = st.chat_input("Ask a question about your college...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Searching college documents and generating an answer..."
        ):
            try:
                result = rag_pipeline.generate_response(question)

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)
                display_sources(sources)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as error:
                st.error(
                    "Sorry, something went wrong while processing "
                    "your question."
                )
                st.caption(str(error))
