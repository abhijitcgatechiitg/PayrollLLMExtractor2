Payroll Data Extraction

Goal: To create a general extraction system for payroll data which can work accross different report types and is able to extract information into a structured global schema system. Global schema is a fixed schema which caters to all report types ideally. 

Given: 
I have provided a few examples in the sample_pdfs folder. 
old_global_schema.md is an idea of how I wanted the global schema to look. It can be edited as we go and we need to track some metadata like pages as well.
One major thing is that these pdfs can have multiple pages so I need to send each page at a time so I don't exceed the token range in LLM. 
I will also provide a code for previous financial data extractor we made, I need to take inspirasion from that but do not make exact same things since some things might be different. You can use this code first to understand what we did previously.


Tech i've planned to use:
- pymupdf for text extraction
- LLM haiku model - claude-haiku-4-5-20251001



Idea: Projcect Pipeline
Step 1 — Extract pdf data into text using pymupdf. Here these is a thing we need to take care of. Since previously when we worked on financial data we had a section identifier after this which will find the exact page where text is and pass it downstream, but now we may have a pdf with multiple pages and we might need to work one page at a time. 
Step2:we will build a two pass system. 
Once we have the text from the pdf, we will then use LLM and a prompt to extract an interim json. This will be a raw extraction of the text and no mapping is done yet. Just a simple read and creating a interim json schema. We might need to give some info to model in how to extract it, please go through previous code to understand that.

Step3: Since we have the interim json now, we will try to map it to the global_schema using another LLM pass. Now this global schema is not a exact replica of the pdf as whole purpose is to build a general solution. Some fields might not be required as well in this global schema. So it's on the model to only populate required fields in the global schema and skip the rest extracted data. 
This mapping strategy needs to be aided by prompt and rules that might help. 
this doing a 2 pass system which helps with accuracy. 
Once it is mapped, it will be saved to a output folder. 
Mapping is done using LLM knowledge of payroll as well as some rules or guidelines in prompt. 
As we do each step, i would like to create a folder for a pdf, that way all the intermidiate and the final output will be saved in a folder by the name of the pdf. 

Note: We don't need to add a validation layer yet, but let's keep a dummy code files there for future work.

Current goal
1. Build a global_schema based on the old_global_schema.md
2. Build all the code struture and code files for this code

