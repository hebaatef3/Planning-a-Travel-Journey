from argparse import ArgumentParser
from gooey import Gooey, GooeyParser
from pyswip import Prolog


swipl = Prolog()
swipl.consult("pro.pl")  

@Gooey
def check_travel():
    parser = GooeyParser(description="Check Travel Options")
    parser.add_argument("-s", "--start", required=True, help="Starting location\n please insert Capital first letter")
    parser.add_argument("-e", "--end", required=True, help="Destination location \n please insert Capital first letter")
    parser.add_argument("-t", "--transport", choices=["train", "plane", "car", "any"], default="any", help="Select transport type (Optional)")

    args = parser.parse_args()

    start_location = args.start
    end_location = args.end
    selected_transport = args.transport

    if selected_transport == "any":
        direct_travel = check_direct_travel_prolog(start_location, end_location)
        if direct_travel:
           print("Direct travel options:")
           for travel in direct_travel:
             print(travel)
           indirect_travel = check_indirect_travel_prolog(start_location, end_location)
           print("\nIndirect travel options:")
           for travel in indirect_travel:
              print(travel)
        else:
            print(f"No Direct travel from {start_location} to {end_location}")
            indirect_travel = check_indirect_travel_prolog(start_location, end_location)
            print("\nIndirect travel options:")
            for travel in indirect_travel:
               print(travel)
    else:
        direct_travel = check_direct_travel_prolog_with_transport(start_location, end_location, selected_transport)
        indirect_travel = check_indirect_travel_prolog(start_location, end_location)

def check_direct_travel_prolog(start, end):
    query = f"can_travel_directly('{start}', '{end}', Transport)."
    return list(swipl.query(query))

def check_direct_travel_prolog_with_transport(start, end, transport):
    query = f"can_travel_directly('{start}', '{end}', '{transport}')."
    travels = list(swipl.query(query))
    if travels:
        print(f"You can travel from {start} "
              f"to {end} "
              f"by {transport}")
    else:
        print(f"No direct travel available from {start} "
              f"to {end} "
              f"by {transport}")
        indirect_travel = check_indirect_travel_prolog(start, end)
        print("\nIndirect travel options:")
        for travel in indirect_travel:
            print(travel)
        return None

def check_indirect_travel_prolog(start, end):
    query = f"can_travel_indirectly('{start}', '{end}', Transports), connection('{start}', Intermediate, Transport1), connection(Intermediate, '{end}', Transport2), Transports = [Transport1, Intermediate, Transport2]."
    results = swipl.query(query)
    indirect_travels = []
    for result in results:
        transport1, intermediate, transport2 = result["Transports"]
        indirect_travels.append((f"From {start} to {intermediate} by {transport1}", f"From {intermediate} to {end} by {transport2}"))
    return indirect_travels


if __name__ == "__main__":
    check_travel()
