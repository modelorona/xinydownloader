# lord help me with this
from uuid import uuid4


def do_work(text, previous_details={}):
    """
        Does a lot of work. Gets the authors, content, and description with shitty parsing
        of the markdown. Will change to use regex later.
        :param text: the markdown text that will get mangled
        :param previous_details: a dictionary which will contain the previous details of the current text
        in case needed
        :return: a dictionary with all the information on the language that is taken from the text
    """
    return_object = dict()
    # the id of the data should be unique. easy to generate as well
    return_object.update({"id": uuid4().hex})
    contributors = {}
    text = str(text)
    # print(text)
    text = text.split('\n')

    # re will have to wait
    # let's get contributors the hard way
    for line in text:
        if line.startswith('    - [') and line.endswith(']'):
            split_line = line.split(',')
            contributors[split_line[0][8:-1]] = split_line[1][2:-2]
    # now we have contributors
    return_object.update({"contributors": contributors})

    # now to get the content
    content = list()
    content.append('```')
    first_found = False  # to handle the start and end code blocks
    for line in text:
        if line.startswith("```"):
            first_found = not first_found
            continue
        if first_found:
            content.append(line)
    content.append('```')
    content = "\n".join(content).strip()
    return_object.update({"content": content})

    # now for the description
    description = list()
    in_recording_mode = False
    for line in text:
        if not in_recording_mode:
            if line.startswith('---'):
                in_recording_mode = True
        elif line.startswith('```'):
            in_recording_mode = False
        else:
            description.append(line)

    description = "\n".join(description).split('---')[1].strip()
    return_object.update({"description": description})

    # fuck the finishing words and the learn now for now

    return return_object

