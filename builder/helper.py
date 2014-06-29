import json

def trim_proper(content, length):
    args = content.split("\t")
    while (len(args) < length): args.append(None)
    
    for i in xrange(0, len(args)):
        col = args[i]

        if (col != None):
            col = col.strip()

            if (len(col) == 0):
                col = None

        args[i] = col

    return args

def write_output(options, output):
    new_json = json.dumps(output)

    if options.is_preview:
        print new_json
        return

    file_path = options.get_output_path("conbook.json")
    output_file = open(file_path, "w")
    output_file.write(new_json)
    output_file.close()
