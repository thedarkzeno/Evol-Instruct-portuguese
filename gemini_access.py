
import google.generativeai as genai
import time

api_key = 'your api key'
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def get_gemini_completion(prompt):

        response = model.generate_content(prompt)
      
        res = " ".join([part.text for part in (response.parts)])
       
        gpt_output = res
        return gpt_output

def call_gemini(ins):
    success = False
    re_try_count = 15
    ans = ''
    while not success and re_try_count >= 0:
        re_try_count -= 1
        try:
            ans = get_gemini_completion(ins)
            success = True
        except:
            time.sleep(5)
            print('retry for sample:', ins)
    return ans
