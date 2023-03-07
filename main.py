import os
#os.environ["OPENAI_API_KEY"] = "..."
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an text that may be poorly worded.
    Your goal is to:
    - Properly format the text
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Dovish: The Federal Open Market Committee (FOMC) has decided to maintain the current target range for the federal funds rate at 0.00-0.25 percent. The Committee sees the current economic environment as challenging, with the labor market still showing signs of weakness and inflation remaining persistently below the Committee's 2 percent objective. Although economic activity has picked up from its depressed second-quarter level, the ongoing public health crisis is causing tremendous human and economic hardship across the United States and around the world. The path of the economy will depend significantly on the course of the virus. In light of these developments, the Committee is committed to using its full range of tools to support the U.S. economy in this challenging time, thereby promoting its maximum employment and price stability goals. The Committee will continue to increase its holdings of Treasury securities and agency mortgage-backed securities at least at the current pace to sustain smooth market functioning and help foster accommodative financial conditions, thereby supporting the flow of credit to households and businesses. The Committee will also continue to closely monitor inflation indicators and global economic and financial developments, and will adjust monetary policy as necessary to foster financial and economic stability.
    - Neutral: The Federal Open Market Committee (FOMC) has decided to maintain the current target range for the federal funds rate at 0.25-0.50 percent. The Committee judges that the labor market has continued to strengthen and that economic activity has been expanding at a moderate pace. However, inflation remains below the Committee's 2 percent longer-run objective, partly reflecting earlier declines in energy prices and in prices of non-energy imports. The Committee expects inflation to remain low in the near term but anticipates that it will rise to 2 percent over the medium term as the transitory effects of past declines in energy and import prices dissipate and the labor market strengthens further. In light of the current economic conditions, the Committee is maintaining its policy of reinvesting principal payments from its holdings of agency debt and agency mortgage-backed securities in agency mortgage-backed securities and of rolling over maturing Treasury securities at auction. The Committee is maintaining its existing policy of reinvesting principal payments from its holdings of agency debt and agency mortgage-backed securities in agency mortgage-backed securities and of rolling over maturing Treasury securities at auction, and it anticipates doing so until normalization of the level of the federal funds rate is well underway. This policy, by keeping the Committee's holdings of longer-term securities at sizable levels, should help maintain accommodative financial conditions.
    - Hawkish: The Federal Open Market Committee (FOMC) has decided to raise the target range for the federal funds rate by 25 basis points to 1.00-1.25 percent. The Committee believes that the labor market has continued to strengthen and that economic activity has been expanding at a solid pace. Inflation measures have increased in recent months and are now close to the Committee's 2 percent longer-run objective. The Committee expects that economic conditions will evolve in a manner that will warrant gradual increases in the federal funds rate, and that such increases will be consistent with sustained expansion of economic activity, strong labor market conditions, and inflation near the Committee's symmetric 2 percent objective over the medium term. The Committee intends to continue to gradually reduce the Federal Reserve's securities holdings in a gradual and predictable manner primarily by ceasing to reinvest repayments of principal on securities held in the System Open Market Account. The Committee expects to begin implementing its balance sheet normalization program relatively soon, provided that the economy evolves broadly as anticipated. The Committee continues to closely monitor inflation indicators and global economic and financial developments, and will adjust monetary policy as necessary to foster financial and economic stability.

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the text with a warm introduction. Add the introduction if you need to.
    
    Below is the text, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    text: {text}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "text"],
    template=template,
)

def load_LLM():
    llm = OpenAI(temperature=.7)
    return llm

llm = load_LLM()


st.set_page_config(page_title="FOMC Text", page_icon=":robot:")
st.header("CENTRAL BANK STATEMENT")

st.markdown("Given how the market weights every word, \
            a central banker needs to convey the right tone in its statement. This \
            tool will help the central banker to craft exactly the right words to reflect dovish, \
            neutral or hawkish tone.")
            
st.markdown("## Enter Your Phrase To Convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your text to have?',
        ('Dovish', 'Neutral', 'Hawkish'))    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="text Input", label_visibility='collapsed', placeholder="Your text...", key="text_input")
    return input_text

text_input = get_text()

if len(text_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

if st.button("Click"):
    if text_input:
        prompt_with_text = prompt.format(tone=option_tone, dialect=option_dialect, text=text_input)
        formatted_text = llm(prompt_with_text)
        st.markdown("## Your Statement:")
        st.write(formatted_text)


