# linkedin-skillbot
Gotta solve em all!

### Usage
Just start and go pretty much. I will add a requirements in the future for now just `pip3 install` whatever python tells you to :)
```
python3 linkedin_parser.py --show --live
```
 - `--show` Opens ChromeDriver in front aka. look how computer make magic and clicky on buttons without doing anything. Otherwise it will start headless.
 - `--live` This sets it to solve actual tests, if not set it will run "practice" (I used this for testing.)
### .env
You should have a `.env` file in the working dir.
```
LINKED_IN_USER=user@name.com
LINKED_IN_PASS=YourPass123!
LINKED_IN_PROFILE=https://www.linkedin.com/in/YOURUSERNAME/
```
### Where it didnt work
This could be, because the answers aren't correct or it didnt find the correct question/answer file.
- Object-Oriented Programming (OOP) Assessment
- Rust (Programming Language) Assessment
- JSON Assessment
- Android Assessment (because of picture answers, it breaks the code right now)
- Django Assessment
- Google Ads Assessment
- Avid Media Composer Assessment
- Cascading Style Sheets (CSS) Assessment
- Microsoft Power Automate Assessment
- Dreamweaver Assessment
- jQuery Assessment 
- Ruby on Rails Assessment
- Pro Tools Assessment
- Transact-SQL (T-SQL) Assessment
- Microsoft Outlook Assessment 
- Microsoft Word Assessment
- Adobe Animate Assessment
- Objective-C Assessment
- Logic Pro Assessment
- Accounting Assessment
- .NET Framework Assessment
- Final Cut Pro Assessment
- Autodesk Maya Assessment (I passed with pure luck, no answers were found)
- Scala Assessment
- R (Programming Language) Assessment
- Adobe XD Assessment 
- After Effects Assessment
- ArcGIS Produts Assessment
- Microsoft Access Assessment
- Microsoft PowerPoint Assessment
- Visual Basic for Applications (VBA) Assessment
- Rhino 3D Assessment
- Microsoft Power BI Assessment 
- Keynote Assessment
- Autodesk Fusion 360 Assessment
- iMovie Assessment
- Adobe Premiere Pro Assessment
- MATLAB Assessment
- Autodesk Inventor Asessment
- Adobe Lightroom Assessment
- Revit Assessment
- QuickBooks Assessment
- 


### TODO:
- [ ] Make Assessment search better (normalize .md files or make selection smarter)
- [ ] Clean answer search (too many different kinds)
- [ ] clean question search (too much bloat)
- [ ] add statistsics (score percentage)
- [ ] collect questiona and answer pairs we do not have (and add to .md format files)
- [ ] add loggin (print is kind of lame)
- [ ] handle multiple choice answers better
- [ ] fix bug when answer includes too much code (the issue is the search, it splits question on newline and the code breaks it in weird chunks since it is displayed with `\n`)
- [ ] fix error when answers are pictture, it'll just crash (IMPORTANT)
- [ ] (optional) add screenshots 
- [x] add a super duper failsafe that searches for the answer in ALL documents

### Things I straight up don't care about here:
- speed, this does not need to be fast, matter of fact, with most scrapers or web automation tools, speed is what gets you caught


