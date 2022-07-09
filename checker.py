import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import os
from subprocess import PIPE, run
from typing import List, Optional
from pydantic import BaseModel


class CheckerResponse(BaseModel):
    success: bool
    error_message: Optional[str]


def tokenize_code(text: str) -> List[str]:
    return word_tokenize(text)

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout, result.stderr


def check_c_sintax(text: str):
    """
    Checks if the syntax is correct
    """

    # guardar el texto como archivo cpp
    with open("file.cpp", "w") as temp_file:
        temp_file.write(text)
    output, error = out("cppcheck file.cpp")

    success = error == ""
    error_message = error
    
    return success, error_message
    

def check_c_function(text: str):
    
    tokens = tokenize_code(text)
    inverse_tokens = tokens[::-1]

    # find the left most bracket
    
    
    # find the right most bracket
    try :
        right_bracket_idx = inverse_tokens.index("}")
        t = inverse_tokens[0:right_bracket_idx]

        if not all([token == ";" for token in t]):
            return False, "It does not end with only ; characters" 
    except:
        return False, "No right bracket found"
    
    # find the left most bracket}
    
    try :
        left_bracket_idx = tokens.index("{")
        t = tokens[0:left_bracket_idx]
        if t.count("(") != 1 or t.count(")") != 1:
            return False, "No ')' or '(' character before first bracket"
        
        if t[2] != "(":
            return False, "No '(' character as a third element"
        
        if ";" in t:
            return False, "Statement before function"
        #if t != ")":
        #    return False, "No ')' character before first bracket"
    
    except:
        return False, "No left bracket found"
    
    
    return True, ""

def code_checker(text: str) -> CheckerResponse:
    # 1. Check the syntax of the input
    print("Checking syntax...")
    success, error_message = check_c_sintax(text)
    
    if not success: 
        return CheckerResponse(
            success=False,
            error_message=error_message
        )
    
    # 2. Check if is a c/c++ function
    print("Checking c/c++ function structure...")
    success, error_message = check_c_function(text)
    
    if not success:
        return CheckerResponse(
            success=False,
            error_message=error_message
        )
    
    return CheckerResponse(
            success=True,
            error_message=None
        )

