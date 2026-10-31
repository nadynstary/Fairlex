"""
for each category, the summarizer will have a different prompt for the LLM (Gemini)
"""
CATEGORIES_PROMPTS = {
    "Educational":("You are an expert in educational contracts. The given document/text is related to educational matters, focus on: what personal data is being collected/academic, what data is shared with the institution/third parties, how long records are kept, and alert the user what fees, penalties, or binding commitements the user is agreeing to. the summary has to be in a clear language using simple words even when using difficult words explain them"),
    "Governmental": ("This is a governmental document/text. Please summarize it focusing on the personal data being collected, what data is going to get shared with what government department, what benefits are the user gaining and for what price (fees, penalties, binding commitements), and explain any agreements or privacy alerts that user might be sceptical about. The summary has to clear, simple while using user-friendly terms"),
    "Financial": ("This contract is related to a financial matter, analyze the text/document and summary of the content of the document. Focus on what personal data is being conducted and at what cost"),
    "Healthcare": ("This is a document related to a healthcare contract, analyze it and give a summary of the content, BE VERY carful and do not bring any unrelated text to the summary, explain it in plain words and focus on any clauses that may concern the user"),
    "Creating a new account": ("The given text was given to a person while creating an account, please analyze and summarize it and highlight any clauses"),
    "Purchasing a product or service":("The given text/document was given to the user during the processs of purchasing or buying an item or service please summarize the text and highlight any clauses that may concern the user"),
    "Employment": ("This text/document was given to a person from their Employer company/organization. Please summarize it and give any security clauses or requirements or legal bindings during the user's time at the comapny, before and after"),
    "Other": ("This text/document was given to the user please analyze it, figure out what is it for and summarize it before higlighting the legal clauses in the contract / text")

}






