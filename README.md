# rekordbox-add-track-comments-from-playlist-name
A Python script designed to streamline the process of editing and organizing my Rekordbox XML library.  
Here is how I organize my playlists (in the collection explorer on the left side of rekordbox):  

Collection   
Playlists  
&emsp;event-playlist  
&emsp;FOLDERS  
&emsp;&emsp;genre-subfolder  
&emsp;&emsp;&emsp;year-playlist  
&emsp;&emsp;genre-playlist  
rekordbox xml  
Histories  
    
This script acts only on the FOLDERS folder, it doesn't act upon event-playlists. First you need to export the rekordbox collection by going to file--> export rekordbox collection as xml  

Functions:  
* Identify Duplicates:  
  * Detects tracks that are in multiple year-playlists within the same genre-subfolder. (this is unwanted, and i can manually fix in rekordbox based on the output).  
  * Tracks can be in multiple genre-playlists or genre-subfolders, but shouldn't be in multiple year-playlists within the same genre-subfolder  

* Update Track Comments:  
  * Append a tag based on the name of the genre-playlists or genre-subfolders containing a track to the track Comments field  
  * Tags can be customized using an abbreviations dictionary.  
  * If a track is in multiple genre-playlists or genre folders, tags are added for each  
  
* Save Updated XML  
  * Prompts the user to save the modified XML to a new file.  

after saving the updated XML, you can import it back into rekordbox  

1. file > preferences > advanced  
2. click 'browse' under 'imported library'  
3. select your generated XML  
4.close out of preferences menu  
5. find the "rekordbox xml" tab on the collection explorer in the  left of the screen. it will show "All Tracks" and "Playlists"  
6. right click on a playlist to import it into your collection.   
7. because there is a bug in rekordbox that prevents importing xml data for tracks that are already in your collection, one further step is required- if you check at this point in your main collection --> playlists you will see the comments have not been updated  
8. The next step is you have to click on "rekordbox xml" tab-->"All Tracks", select all the tracks, and import them all back into your rekordbox collection (right click on one selected track to do this).  
[this video](https://youtu.be/xzW0jHWSNPk) explains how to do it 
