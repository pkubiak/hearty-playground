# Hearty Playground #

## Features ##

- Markdown
  - Advanced Custom markdown editor 
  - Configured many markdown features
  - templatetag for consistend markdown rendering
  
- User management
  - User creation
  - Custom user class (with email, avatar)
  - Simple user panel
  - Statistics
    - User progress monitoring
  - Achievements
    - Possibility to define own achievements (colors, icons, text)
    - as for now only manual acquisition
- Course and lessons
  - grouping activities into courses and lessons
- Activities
  - Extensible architeture based on django apps and MTI via polymorphics models
  - Polymorphic routing
  - Progress Counting
  - ActivityNote
    - Simple completable activity
  - ActivityQuiz
    - Three types of questions
      - single answer
      - multi answer
      - open answer
    - multiple attempts
    - full markdown rendering
    - score counting
    
- Admin panel
  - creating course, lessons, activities
  
- Help module
  - possibility to create static pages with help (in markdown)
  
 

### Planned Views ###

| name         | status |
|--------------|--------|
| landing pace | - |
| login        | implemented |
| profile      | partialy implemented |
| task list    | implemented |
| courses      | implemented |
| ActivityNote | implemented |
| ActivityQuiz | implemented |
| ActivityWorkspace | mocked |
| workspace    | mocked |
| help         | implemented |

### 2020-01-23 - Quiz Activity ###
![](mockup/Screenshot_2020-01-23_11-52-02.png)


[![Watch the video](https://img.youtube.com/vi/xE4JCkFqSBg/0.jpg)](https://youtu.be/xE4JCkFqSBg)

[Youtube video: https://youtu.be/xE4JCkFqSBg](https://youtu.be/xE4JCkFqSBg)

### 2020-01-23 - User statistics ###
![](mockup/Screenshot_2020-01-23_03-59-36.png)

### 2020-01-16 - Course Details ###
![](mockup/Screenshot_2020-01-16_01-18-17.png)

### 2020-01-09 - Courses View ###
![](mockup/Screenshot_2020-01-09_04-46-00.png)

### 2019-12-06 - Workspace View ###
![](mockup/Screenshot_2019-12-06_03-17-13.png)
