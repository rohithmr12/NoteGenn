from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

def generate_llama_response(input_text, no_words):
    llm = CTransformers(model='llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.5})

    template = """
        this is a part of a lecture turn use this and make notes for this topic and keep in mind many small instances like this are happening right now with the continuation to this text soo dont go overboard{input_text}
    """

    prompt = PromptTemplate(input_variables=["input_text"],
                            template=template)

    # Generate the response from the LLama 2 model
    response = llm(prompt.format(input_text=input_text, no_words=no_words))
    
    return response

