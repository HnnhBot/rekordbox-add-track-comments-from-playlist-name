import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog
def update_comments(root, track_tag="TRACK"):
    """
    Updates the comment field of tracks in Rekordbox XML based on folder or playlist hierarchy, 
    ensuring changes are applied to the actual track data in the <COLLECTION> section.

    Parameters:
    - root: The root XML node of the entire Rekordbox XML tree.
    - track_tag: XML tag representing tracks (default: "TRACK").
    """
    # Define abbreviations
    abbreviations = {
        "Hnnh deep dub": "deep dub",
        "bootay space booty": "space booty",
        "bootyclubbreaks dark": "BCB dark",
        "bootyclubbreaks MELODIC": "BCB melodic",
        "bootyclubbreaks PERCUSSIVE": "BCB percussive",
        "bass bump/minimal punch": "BB/min",
        "Bongo Tech house": "bongo",
        "GTechHaus badland": "Gtech",
        "Playa/ late night/dubtechno": "playa/LN",
        "Cuntry hoe down shit": "cuntry",
    }

    # Step 1: Map Track IDs to Tags (Playlist or Folder Names)
    track_to_tags = {}  # Map of TrackID -> [tags]
    folders_node = None

    # Locate the FOLDERS node
    for node in root.findall(".//NODE"):
        if node.get("Name") == "FOLDERS":
            folders_node = node
            break

    if not folders_node:
        print("FOLDERS node not found. Exiting.")
        return

    # Traverse playlists and folders
    for node in folders_node.findall("./NODE"):
        parent_name = node.get("Name")
        node_type = node.get("Type")

        # Skip numeric names or "Slow BPM"
        if parent_name.isdigit() or parent_name.lower() == "slow bpm":
            continue

        # If it's a playlist, add its tag to associated tracks
        if node_type == "1":  # Playlist
            playlist_tag = abbreviations.get(parent_name, parent_name)  # Use abbreviation or full name
            for track in node.findall(f".//{track_tag}"):
                key = track.get("Key")
                if key:
                    track_to_tags.setdefault(key, []).append(playlist_tag)

        # If it's a folder, process its sub-playlists
        elif node_type == "0":  # Folder
            folder_tag = abbreviations.get(parent_name, parent_name)  # Use abbreviation or full name
            for sub_node in node.findall("./NODE"):
                if sub_node.get("Type") == "1":  # Sub-node is a playlist
                    for track in sub_node.findall(f".//{track_tag}"):
                        key = track.get("Key")
                        if key:
                            track_to_tags.setdefault(key, []).append(folder_tag)
    print(f"Track-to-Tags Mapping: {track_to_tags}")

    # Step 2: Update Tracks in <COLLECTION>
    collection_node = root.find(".//COLLECTION")
    if not collection_node:
        print("<COLLECTION> node not found. Exiting.")
        return

    for track in collection_node.findall(f".//{track_tag}"):
        track_id = track.get("TrackID")
        if track_id in track_to_tags:
            tags = " ".join(track_to_tags[track_id])
            current_comment = track.get("Comments", "").strip()
            print(f"Current Comments: {current_comment}, New Tags: {tags}")  # Debugging
            if tags not in current_comment:
                updated_comment = f"{tags} // {current_comment}".strip()
                track.set("Comments", updated_comment)
                print(f"Updated track {track_id} with comment: {updated_comment}")

def identify_duplicates(root, folders_node, track_tag="TRACK"):
    """
    Identifies tracks that are in multiple playlists within the same folder and prints their details,
    including the track name and dateAdded from the <COLLECTION> section.

    Parameters:
    - root: The root XML node of the entire Rekordbox XML tree.
    - folders_node: The <FOLDERS> node from the XML structure.
    - track_tag: XML tag representing tracks (default: "TRACK").
    """
    # Locate the COLLECTION node
    collection_node = root.find(".//COLLECTION")
    if not collection_node:
        print("<COLLECTION> node not found. Exiting.")
        return

    # Build a map of TrackID -> {Name, DateAdded}
    track_data = {}
    for track in collection_node.findall(f".//{track_tag}"):
        track_id = track.get("TrackID")
        track_name = track.get("Name", "Unknown Name")
        date_added = track.get("DateAdded", "Unknown Date")
        if track_id:
            track_data[track_id] = {"Name": track_name, "DateAdded": date_added}

    # Tracks in multiple playlists within the same folder
    duplicates = []

    # Traverse folders
    for folder in folders_node.findall("./NODE"):  # Top-level folders
        folder_name = folder.get("Name")
        folder_tracks = {}  # Map of Track Key -> [playlist names]

        for playlist in folder.findall("./NODE"):  # Playlists within this folder
            if playlist.get("Type") == "1":  # Playlist
                playlist_name = playlist.get("Name")
                for track in playlist.findall(f".//{track_tag}"):
                    key = track.get("Key")  # Use Key for playlist tracks
                    if key:
                        # Add playlist name to track's list
                        if key not in folder_tracks:
                            folder_tracks[key] = []
                        folder_tracks[key].append(playlist_name)

        # Check for duplicates within this folder
        for key, playlists in folder_tracks.items():
            if len(playlists) > 1:  # Found a duplicate
                track_info = track_data.get(key, {"Name": "Unknown Name", "DateAdded": "Unknown Date"})
                duplicates.append({
                    "TrackName": track_info["Name"],
                    "DateAdded": track_info["DateAdded"],
                    "Playlists": playlists,
                    "Folder": folder_name,
                })

    # Print duplicates
    if duplicates:
        print("\nTracks in multiple playlists within the same folder:")
        for dup in duplicates:
            print(f"Track Name: {dup['TrackName']}")
            print(f"Date Added: {dup['DateAdded']}")
            print(f"Folder: {dup['Folder']}")
            print(f"Playlists: {', '.join(dup['Playlists'])}\n")
    else:
        print("No duplicates found.")

def select_xml_file():
    """
    Opens a file dialog to select an XML file and returns the file path.
    """
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Rekordbox XML File",
        filetypes=[("XML Files", "*.xml")]
    )
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected.")
        return None
    
def parse_xml(file_path):
    """
    Parses the selected XML file and returns the root element.
    """
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError:
        print("Error parsing the XML file. Please ensure the file is valid.")
        return None

def save_updated_xml(tree):
    """
    Opens a file dialog to save the updated XML file.
    """
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        title="Save Updated XML File",
        defaultextension=".xml",
        filetypes=[("XML Files", "*.xml")]
    )
    if file_path:
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)
        print(f"Updated XML file saved to: {file_path}")
    else:
        print("Save operation cancelled. No changes were written.")

if __name__ == "__main__":
    # Step 1: Select XML file
    xml_file_path = select_xml_file()
    if not xml_file_path:
        exit()

    # Step 2: Parse the XML file
    tree = parse_xml(xml_file_path)
    if not tree:
        exit()

    # Step 3: Locate FOLDERS node
    root = tree.getroot()
    folders_node = None
    for node in root.findall(".//NODE"):
        if node.get("Name") == "FOLDERS":
            folders_node = node
            break

    if not folders_node:
        print("FOLDERS node not found. Exiting.")
        exit()

    # Step 4: Identify duplicates (runs before updating comments)
    print("Checking for duplicates...")
    identify_duplicates(root, folders_node)

    # Step 5: Edit the XML
    print("Updating comments...")
    update_comments(root)

    # Step 6: Save the updated XML file
    save_updated_xml(tree)
