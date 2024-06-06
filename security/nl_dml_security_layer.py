import re
update_pat = r'upda?te|upd[4a]t[3e]'
insert_pat = r'[i!]n[s5][e3]r[t7]'
remove_pat = r'r[e3]m[o0]v[e3]'
delete_pat = r'd[e3][l!][e3][t7][e3]'
class NL_SECURITY_LAYER:
    
    def __init__(self, user_input) -> None:
        self._user_input:str = user_input
        self._dml_sql_nl_keywords: dict = {"update": update_pat, "insert": insert_pat, "remove": remove_pat, "delete":delete_pat}

        # Flag for user DML statements
        self._is_dml_input: bool = False

    # getters
    def get_user_input(self) -> str:
        return self._user_input
    def get_user_input_list(self) -> list[str]:
        return self._user_input_list
    def get_is_dml_input(self) -> bool:
        return self._is_dml_input
        
    def _clean_words(self) -> None:
        user_input = self._user_input

        #convert all to lowercase
        user_input=user_input.lower() 

        #remove symbols
        user_input = re.sub('''[!@#$?",']''', "", user_input)

        #read to self
        self._user_input_list = user_input.split(" ")
        self._user_input= user_input


    def _filter_nl_prompt(self):
        user_input_list = self._user_input_list
        user_dml_keywords = []
        for base_dml_keyword, pattern in self._dml_sql_nl_keywords.items():
            for token in user_input_list:
                if re.search(pattern, token):
                    user_dml_keywords.append(base_dml_keyword)
                    self._is_dml_input = True
                # if (dml_keyword in token) and (token not in user_dml_keywords):
                #     user_dml_keywords.append(dml_keyword)
                #     self._is_dml_input = True


        self._user_dml_keywords = user_dml_keywords

    def _warn_user(self):
        return(f'''
I am not able to process this input.
You have used the following keywords in some way: {self._user_dml_keywords}.
I am not allowed to alter the data using these commands
Please change the intention of your request''')    
    
    def protect_input(self):
        self._clean_words()
        self._filter_nl_prompt()
        if self._is_dml_input:
            return(self._warn_user())
        else:
            return False
