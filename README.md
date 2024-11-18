# rekordbox-add-track-comments-from-playlist-name
A Python script designed to streamline the process of editing and organizing my Rekordbox XML library.  
Here is how I organize my playlists:  

Collection   
Playlists  
  event-playlist  
  FOLDERS  
    genre-subfolder  
      year-playlist  
    genre-playlist  
rekordbox xml  
Histories  
    
This script acts only on the FOLDERS folder, it doesn't act upon event-playlists. First you need to export the rekordbox collection by going to file--> export rekordbox collection as xml  

Functions:  
Identify Duplicates:  
  Detects tracks that are in multiple year-playlists within the same genre-subfolder. (this is unwanted, and i can manually fix in rekordbox based on the output).  
  Tracks can be in multiple genre-playlists or genre-subfolders, but shouldn't be in multiple year-playlists within the same genre-subfolder  

Update Track Comments:  
  Append a tag based on the name of the genre-playlist or genre-subfolder containing a track to the track Comments field  
  Tags can be customized using an abbreviations dictionary.  
  If a track is in multiple genre-playlists or genre folders, tags are added for each  
  
Save Updated XML  
  Prompts the user to save the modified XML to a new file.  

after saving the updated XML, you can import it back into rekordbox  

file > preferences > advanced  
click 'browse' under 'imported library'  
select your generated XML  
close out of preferences menu  
find the "rekordbox xml" tab on the collection explorer in the bottom left of the screen. it will show "All Tracks" and "Playlists"  
right click on a playlist to import it into your collection.   
because there is a bug in rekordbox that prevents importing xml data for tracks that are already in your collection, one further step is required. if you check at this point in your main collection --> playlists you will see the comments have not been updated  
The nexy step is you have to click on rekordbox xml-->"All Tracks", select all the tracks, and import all the tracks back into your rekordbox library (right click on one track to do this).
