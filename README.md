# Title of the project : Write It

## Video Demo : [CS50 Final Project || Write It](https://www.youtube.com/watch?v=NDQnLuu0sFE&t=148s)

My final project is a webapp that lets you make diaries and notes.

Everything implemented in the project was done from scratch whether the design or the functionality of it.

And this is a thorough elaboration of how it works and what it does.

## index.html

The index page is where you get redirected when you first open the site and you're not logged in.

It's the page that shows the user the features of the program.

It also has a section at the end that has some info about me and why I did this project

## signup.html

The user can register and have a new account by visiting the sign up page.

There's some limitations to this process:
- The username must not used by any other users and must not contain any spaces.
- The password must be 8 characters or more, it must be identical to the confirmation field and must have lowercase and uppercase letters.
- Both of the phone and the email must not be used by any other users.

## signin.html

That is where the user can sign in to their account.

If the username or the password is incorrect, it won't sign the user in.

But if they're correct, it will sign the user only if they're not already logged in on other device.

## home.html

When the user sign in, they get redirected to the home page which displays some of the statistics like how many notes or diary the user have made .

And of course the app get those statistics from the database that records almost everything.

## notes.html

If the user wants to make a note, the user can open the notes page

So all the user have to do is to click a button, write what they want and then hit the make button.

But after the user do that the note that they with get displayed in the page.

The user can edit the note, delete it or open it if it's so long

## diary.html

If the user wants to make a diary, the user can open the diary page and it's similar to the process of making a note.

When the user write their diary, the button disappears and doesn't come out again unless in the other day or if the user deleted the current diary because simply i'm supposing that nobody makes more than one diary a day.

## settings.html

In the settings page,

The user can find some of their account's information and also some of their personal information.

The user doesn't have to specify the his personal info

There's also this section at the bottom where the user can delete their account

But anything the user modify in this page requires them to know the password, otherwise it won't modify anything.
