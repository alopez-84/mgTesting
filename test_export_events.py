from re import I
import re
from urllib import response
import requests
import csv

print("This script was written to export a domain's events \n"
    "to a csv file. You will be asked to provide the API key and \n"
    "the domains, as well as your parameters for the request")

api_key = input("Enter your API key: ")

# function to build the request. 
def add_param(params):
    
    options = {
        "1" : "add a start date",
        "2" : "add an end date",
        "3" : "add event type",
        "4" : "add a specific recipient",
    }
    
    # display the users options
    for option in options:
        print(f"[{option}] {options[option]}")

    param_choice = input("What Parameter are you adding? ")
    
    if param_choice == "1":
        begin_date = input("Enter the start date (ex: Thu, 13 Oct 2011 18:02:00 +0000): ")
        params.update({"begin":f"{begin_date}"})
    elif param_choice == "2":
        end_date = input("Enter the end date (ex: Thu, 13 Oct 2011 18:02:00 +0000): ")
        params.update({"end":f"{end_date}"})
    elif param_choice == "3":
        event = input("Enter the event(s) you wish to poll: ")
        params.update({"event":f"{event}"})
    elif param_choice == "4":
        recipient = input("Enter the recipeint: ")
        params.update({"recipient":f"{recipient}"})
    
    return params

#fucntion to get the logs based on the request
def get_logs(domain, r_params):
    return requests.get(
        f"https://api.mailgun.net/v3/{domain}/events",
        auth=("api", api_key),
        params=r_params)

## handles of the logic when writing the JSON to a CSV file
def write_to_csv(resp_json):
    
    #since the response contains a dictionary, one index being 
    # the actial data and the other of the paging URLs
    items = resp_json["items"]

    # create the CSV, yes I know there is the csv library however since each character
    # in the string was treated as it's own cell within the CSV without a delimiter, it was not
    # super readable, also assuming that the customer wants to search and manipulate the data
    # or search it in their logs, the built in file writer was more ideal

    file = open("test_full_script.csv", "w")


    #handle event types of items in the list
    for i in range(len(items)):
        for k, v in items[i].items():
            if isinstance(v, dict):
                write_inner_dict(file, v)
            elif v is None:
                file.write("-\n")
            else:
                file.write(f"\"{str(v)}\"\n, {type(v)}\n")
        file.write(" \n")
        

    file.close()

# Since the response can contain dictionaries within in dictionaries, this function handles that
# by itering through the sub-dictionary as many times as needed and writing to the file.
def write_inner_dict(file, value):
    for k,v in value.items():
        if isinstance(v, dict):
            write_inner_dict(file, v)
        else:
            file.write(f"\"{str(v)}\"\n, {type(v)}\n")
    

def main():

    domain = input("Enter the domain to poll events from: ")

    # since larger customers will likely be doing this, 
    # I am adding the preset parameters of ascending and 300
    # (our limit). That way if they provide no parameters,
    # all events can be pulled using add_params() function.

    request_params = {"limit": 300}
    order = input("Ascending or Descending?").lower()
    
    while True:
        if order == "ascending":
            request_params.update({"ascending":"yes"})
            break
        elif order == "descending":
            break
        else:
            print("That is not a valid input.")
            order = input("Ascending or Descending?").lower()
    



    add_param(request_params)

    resp = input("Do you want to add more parameters? (Y/N): ").upper()
    while True:
        if resp == 'Y':
            add_param(request_params)
            resp = input("Do you want to add more parameters? (Y/N): ").upper()
        elif resp == 'N':
            break
        else:
            resp = input("Please enter a valid input (Y/N): ").upper()

    print(f"Your curent request Paramaters are: {request_params}")

    r = get_logs(domain, request_params)
    print(f"status: {r.status_code}")

    write_to_csv(r.json())

if __name__ == "__main__":
    main()


#future albert
# to do:
# 2. I swear to god we will get to paging 