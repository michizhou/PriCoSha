# PriCoShaDB
To Run (Setup Commands and Tasks) :
- pip3 install flask
- pip3 install pymysql
- import table definitions into mySQL phpAdmin
- python3 app.py in project root directory

PriCoSha is a system for privately sharing content items among groups of people. As a service, PriCoSha grants users more privacy than other content sharing sites by giving them more detailed autonomy over who can see which content items they
post and more control over whether other people can tag content items with a user’s personal information. Our version of PriCoSha focuses on photos and text-based posts for activities like social and professional events. The focus of our project is on storing content data, allowing users to specify who can see and/or modify what, and providing ways for users to find content of interest. Our PriCoSha implementation allows users to log in, post content items, view content items that are public or shared with social groups to which they belong, and propose to tag content items with the e-mails of other users  (provided that content items are visible to both the user (the tagger) and the person being tagged (the taggee)), and manage tag proposals. Each registered user has both a username and password, which is stored as an SHA-2 hash. Some of the extra features of our implementation are as follows:

- Sign Up Page: Lets new users sign up and log in to the app.

- Adding Comments: Users have the option to add comments about content visible to them (i.e. public or shared to groups they are a part of). Data being stored for the comments includes the user who posted them, the content itself, and their timestamps (all of this data is also displayed). By default, all comments are public unless the user who posts the comment indicates otherwise. 

- Defriend: Allows users to defriend one of their existing friends, which involves removing all traces of their former relationship from the database. This would entail removing the defriended person from all friend groups owned by the user who defriended them and removing all tags with the email of the defriended user as the taggee made by the defriending user as the tagger for content items in the friend groups they own.

- Tagging a Group: Users have the option to tag multiple people from a single friend group together in a content item shared between them. This type of tag will only be visible if all of them agree to make it visible by accepting the tag.

- Poking: Users can send a person a message saying they “poked” them. A fun feature from Facebook we thought would be nice to add. If someone has not posted in a while and you would like to hear from a user can poke them. It serves as interesting way to get certain people’s attention and interact with them beyond the scope of messages and normal posts. It also provides a sort of playful atmosphere to the social media experience.
 
- Best Friends: Make a list of each person’s best friends. Allows users to choose specific individuals that they want most closely to follow and allows them to see that person’s posts first before those of their other friends. This feature will introduce some personalization into the user experience by filtering through friends’ posts and prioritizing those of their best friends. It will also seek to strengthen bonds between best friends by having them be more interested and engaged in each other’s posts, which will encourage more use of the social media platform.
 
- Family: Make a list of a person’s family. Similar to best friends but just allows users to specially distinguish people they follow. This feature will also introduce personalization into the user experience, like with the best friends feature, but with family members and relatives on social media. By promoting more user engagement through interactions online between family members and relatives, it will also encourage more usage.
 
- Removing Groups: Allows users to delete friend groups they no longer want. This feature will give users a degree of autonomy and freedom by giving them the choice to exit out of specific friend groups they are no longer interested in and don’t feel comfortable with, which is especially important given the fact that inclusion in friend groups is dictated by invitation at the discretion of the friend groups’ owners. Thus, this feature will ensure that users of a friend group will also have to choice to stay or leave their friend groups on their own terms.

<!---### Acknowledgements for Features--->

<!--- - Maia Litzenberg: user interface/back end integration, content display, log in/out, sign up, add new content, new friend group, add friend to friend group, best friends module (adding and removing)

<!--- - De'Ane Kennedy: manage tags, tagging content items, user interface for tag management

<!--- - Michael Zhou: adding comments, tagging group, user leaves from group, defriending, list of pokes display

<!--- - Jonathan Avila: poking

<!--- - Malcolm: family
