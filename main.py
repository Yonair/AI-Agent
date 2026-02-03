import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import sys



def generate_content(client, messages, verbose):
   
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    function_results = []

    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is not available.")

    if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        pass
    
    
    else:

        for function_call in response.function_calls:
            
            function_call_result = call_function(function_call, verbose=verbose)
            
            if not function_call_result.parts:
               raise Exception("Function call result has no parts.")
            
            first_part = function_call_result.parts[0]

            if first_part.function_response is None:
                raise Exception("Function call returned no function_response")

            response_dict = first_part.function_response.response

            if response_dict is None:
                raise Exception("Function call returned empty response")

            function_results.append(first_part)

            if verbose:
                print(f"-> {response_dict['result']}")
        
    return response, function_results

    

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
        

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

    client = genai.Client(api_key=api_key)

        
    parser = argparse.ArgumentParser(description="Gemini API")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
        

    messages = [types.Content(
        role="user",
        parts=[types.Part(text=args.user_prompt)])]

    
    prompt = args.user_prompt


    if args.verbose:
        print("User prompt:", prompt)

    finished = False
    last_response = None

    for _ in range(20):   
        response, function_results = generate_content(client, messages, args.verbose)
        last_response = response
        for candidate in response.candidates:
            messages.append(candidate.content)
        
        if function_results:
            messages.append(types.Content(
                role="user",
                parts=function_results)
             )
        if not response.function_calls:
            finished = True
            break
    if finished:
        print("Final response:")
        print(last_response.text)
    else:
        print("Agent did not produce a final response within the iteration limit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
