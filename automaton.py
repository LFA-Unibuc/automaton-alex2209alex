from asyncio.windows_events import NULL
from pickle import NONE


class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file
        print("Hi, I'm an automaton!")

    Sigma = ""
    S_state = ""
    F_states = ""
    Transitions = dict()

    def validate(self):
        sigma = False
        states = False
        transitions = False
        Sigma = []
        States = []
        F_states = []
        S_states = []
        Transitions = []
        precedent = dict()
        in_sigma = False
        in_states = False
        in_transitions = False
        line_number = 1
        for line in self.config_file:
            words = [x.strip() for x in line.replace(",", " ").split()]
            #print(words)
            if words[0][0] == "#" and (in_sigma or in_states or in_transitions):
                return f"Comment in invalid position on line {line_number}"
            elif words[0][0] != "#":
                if words[0] == "End" and(not (in_sigma or in_states or in_transitions)):
                    return f"End on invalid position on line {line_number}"
                elif words[0] == "End":
                    in_sigma = False
                    in_states = False
                    in_transitions = False
                elif words[0] == "Sigma" and words[1] == ":" and not sigma:
                    if in_states or in_transitions:
                        return f"Sigma on invalid position on line {line_number}"
                    sigma = True
                    in_sigma = True
                elif words[0] == "Sigma" and words[1] == ":" and sigma:
                    return f"Sigma section appears for second time on line {line_number}"
                elif words[0] == "States" and words[1] == ":" and not states:
                    if in_sigma or in_transitions:
                        return f"States on invalid position on line {line_number}"
                    states = True
                    in_states = True
                elif words[0] == "States" and words[1] == ":" and states:
                    return f"States section appears for second time on line {line_number}"
                elif words[0] == "Transitions" and words[1] == ":" and not transitions:
                    if in_sigma or in_states:
                        return f"Transitions on invalid position on line {line_number}"
                    transitions = True
                    in_transitions = True
                elif words[0] == "Transitions" and words[1] == ":" and transitions:
                    return f"Transitions section appears for second time on line {line_number}"
                elif in_sigma:
                    if len(words) != 1:
                        return f"Invalid sigma input on line {line_number}"
                    if words[0] in Sigma:
                        return f"Duplicated word in sigma on line {line_number}"
                    Sigma.append(words[0])
                elif in_states:
                    if words[0] in States:
                        return f"Duplicated word in states on line {line_number}"
                    if len(words) == 1:
                        States.append(words[0])
                    elif len(words) == 2 and words[1] == "F":
                        States.append(words[0])
                        F_states.append(words[0])
                    elif len(words) == 2 and words[1] == "S":
                        States.append(words[0])
                        S_states.append(words[0])
                    elif len(words) == 3 and ((words[1] == "F" and words[2] == "S") or (words[2] == "F" and words[1] == "S")):
                        States.append(words[0])
                        F_states.append(words[0])
                        S_states.append(words[0])
                    else:
                        return f"Invalid state on line {line_number}"
                elif in_transitions:
                    if len(words) != 3:
                        return f"Invalid transition on line {line_number}"
                    else:
                        Transitions.append([words[0], words[1], words[2]])
                        try:
                            self.Transitions[words[0]].append([words[1], words[2]])
                        except:
                            self.Transitions[words[0]] = []
                            self.Transitions[words[0]].append([words[1], words[2]])
                else:
                    return f"Invalid line {line_number}"
            line_number += 1
        if len(S_states) > 1:
            return "To many states succeded by S"
        self.S_state = S_states[0]
        self.F_states = F_states
        if not sigma:
            return "No sigma"
        if not states:
            return "No states"
        if not transitions:
            return "No transitions"
        if in_sigma:
            return "Sigma not closed"
        if in_states:
            return "States not closed"
        if in_transitions:
            return "Transitions not closed"
        for transaction in Transitions:
            word = transaction[1]
            state_a = transaction[0]
            state_b = transaction[2]
            if word not in Sigma or state_a not in States or state_b not in States:
                return f"Invalid transaction {state_a} {word} {state_b}"
            if state_b in S_states and state_b in precedent.keys():
                if precedent[state_b] != state_a:
                    return f"Invalid transaction {state_b} is a S state and it succeds more than one state"
            if state_b in S_states:
                precedent[state_b] = state_a
        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass

    def read_input(self, input_str):
        """Return the automaton's final configuration

        If the input is rejected, the method raises a
        RejectionException.
        """
        pass


if __name__ == "__main__":
    file = open("a.in", "r")
    a = Automaton(file)
    print(a.validate())
