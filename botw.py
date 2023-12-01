import streamlit as st
import requests

url = "https://botw-compendium.herokuapp.com/api/v3/compendium/"
r = requests.get(url)
botw_data = r.json()

def side_section():
    places_list = []
    for item_dict in botw_data["data"]:
        if item_dict["common_locations"] != None:
            if item_dict["category"] == "equipment":
                for region in item_dict["common_locations"]:
                    if region not in places_list:
                        places_list.append(region)
                        
    return sorted(places_list)

places_list = side_section()

def display(botw_data, location, attack, defense, max_strength):
    possible_list = []
    for item_dict in botw_data["data"]:
        if item_dict["category"] == "equipment" and item_dict["common_locations"] != None:
            if location in item_dict["common_locations"]:
                if item_dict["properties"]["attack"] != None and item_dict["properties"]["defense"] != None :
                    if attack == True and defense == True:
                        if item_dict["properties"]["attack"] <= max_strength and item_dict["properties"]["defense"]:
                            possible_list.append(item_dict)
                    elif attack == True:
                        if item_dict["properties"]["attack"] <= max_strength and item_dict["properties"]["attack"] > 0:
                            possible_list.append(item_dict)
                    elif defense == True:
                       if item_dict["properties"]["defense"] <= max_strength and item_dict["properties"]["defense"] > 0:
                            possible_list.append(item_dict)
    if len(possible_list) == 0:
        st.write("Nothing available for you. Go to Hyrule Field and farm more rupees.")
        
    for item_dict in possible_list:
            st.subheader(item_dict["name"])
            st.image(item_dict["image"], width=300)
            st.write(item_dict["description"])
            if item_dict["properties"]["attack"] > item_dict["properties"]["defense"]:
                rupees = item_dict["properties"]["attack"] * 4
            elif item_dict["properties"]["defense"] > item_dict["properties"]["attack"]:
                rupees = item_dict["properties"]["defense"] * 4
            st.write("This item is for sale for {} Rupees!".format(rupees))
            if rupees <= 5:
                st.image("images/blue_rupee.png", width= 100)
            elif rupees <= 20:
                st.image("images/red_rupee.png", width= 100)
            elif rupees <= 50:
                st.image("images/purple_rupee.png", width= 100)
            elif rupees > 50:
                st.image("images/silver_rupee.png", width= 100)
            st.write("---")
    

max_strength = 0
st.sidebar.header("Beedle's Bazaar")
location = st.sidebar.selectbox("Choose your region: ", places_list)#NEW
st.sidebar.write("Choose equipment type")
attack = st.sidebar.checkbox("Attack")#NEW
defense = st.sidebar.checkbox("Defense")
cost = st.sidebar.slider("Max Price: ",20, 500)#NEW
st.sidebar.text("{} Rupees".format(cost))
if cost > 50:
    max_strength = cost // 5
else:
    max_strength = cost // 10     
begin = st.sidebar.button("Show me equipment options!")
if begin == True:
    display(botw_data,location, attack, defense, max_strength)




    
    

