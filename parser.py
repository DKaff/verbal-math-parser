import sys

class BracketlessTranspiler:
    def __init__(self):
        # Lexicon mappings for logic, flow, and delimiters
        self.lexicon = {
            "equals": "=",
            "cup": "U",
            "cap": "cap",
            "in": "in",
            "greater": ">",
            "than": "",
            "comma": ",",
            "bar": "|",
            "yields": "yields",
            "therefore": "Therefore",
            "hence": "Hence",
            "qed": "Q.E.D.",
            "for": "For",
            "all": "all",
            "exists": "exists",
            "if": "If",
            "then": "then",
            "let": "Let"
        }

    def transpile(self, text_input):
        tokens = text_input.strip().split()
        output = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i].lower()
            
            # --- MODIFIERS ---
            if token == "big":
                if i + 1 < len(tokens):
                    output.append(tokens[i+1].upper())
                    i += 2
                continue
                
            # --- SCOPE MANAGEMENT (Grouping) ---
            elif token == "of":
                # Handle indexed grouping (e.g., 'of sub 1' -> '[')
                if i + 2 < len(tokens) and tokens[i+1] == "sub" and tokens[i+2].isdigit():
                    output.append("[")
                    i += 3
                else:
                    output.append("(")
                    i += 1
                continue
                
            elif token == "to":
                # Handle indexed closing (e.g., 'to sub 1' -> ']')
                if i + 2 < len(tokens) and tokens[i+1] == "sub" and tokens[i+2].isdigit():
                    output.append("]")
                    i += 3
                else:
                    output.append(")")
                    i += 1
                continue
                
            # --- NAVIGATION & POSITIONING ---
            elif token == "sub":
                # Collect subscript items until a 'back' or a delimiter
                sub_tokens = []
                i += 1
                while i < len(tokens) and tokens[i] not in ["back", "yields", "equals"]:
                    if tokens[i] == "comma":
                        sub_tokens.append(",")
                    else:
                        sub_tokens.append(tokens[i])
                    i += 1
                output.append(f"_{{{''.join(sub_tokens)}}}")
                continue
                
            elif token == "sup":
                if i + 1 < len(tokens):
                    output.append(f"^{tokens[i+1]}")
                    i += 2
                continue
                
            elif token == "back":
                i += 1 # Scope pop, acts as a structural boundary
                continue
                
            # --- LOGIC & DELIMITERS ---
            elif token in self.lexicon:
                val = self.lexicon[token]
                if val: # Skip empty mappings like 'than'
                    output.append(val)
                i += 1
                continue
                
            # --- DEFAULT PASS-THROUGH ---
            else:
                output.append(token)
                i += 1

        # Post-process formatting for clean ASCII spacing
        final_string = " ".join(output)
        final_string = final_string.replace("( ", "(").replace(" )", ")")
        final_string = final_string.replace("[ ", "[").replace(" ]", "]")
        final_string = final_string.replace(" ,", ",")
        return final_string

if __name__ == "__main__":
    parser = BracketlessTranspiler()
    
    # Master System Demonstration from Specification
    test_lines = [
        "let big s equals of big a cup big b to cap big c",
        "for all x in big s comma exists y in big b",
        "if x greater than 0 then let big m equals of sub 1 of x comma 1 bar y to comma of y sup 2 back comma 0 bar x to to sub 1",
        "therefore big m sub 2 comma 1 back yields y sup 2",
        "hence qed"
    ]
    
    print("--- Linear Syntax Parsing Demonstration ---")
    for line in test_lines:
        print(f"INPUT:  {line}")
        print(f"OUTPUT: {parser.transpile(line)}\n")