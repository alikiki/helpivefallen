# helpivefallen

`helpivefallen` is a personal knowledge tool that I use to take notes, write down small diary entries, and create flashcards on the fly. 

All the notes, diaries, and flashcard entries are purposefully **append-only**. The point isn't to have a pristine set of notes that I can import to my local machine - it's to capture thoughts and learnings on the fly so that I can go back and review/edit them at the day's end. The editing session in and of itself is integral to how I remember things, so the tool embeds this behavior into its usage model. 

## Commands

`/define [WORD]`: defines a word using GPT-3.5; only defines the first word. Overkill? Probably. 

`/explain [CONCEPT]`: explains a concept using GPT-3.5. Can take multiple words. 

`/qa [QUESTION]??[ANSWER]`: saves a question-answer flashcard. The argument needs to be in the form `[QUESTION]??[ANSWER]`.

`/note [NOTE]`: save a note.

`/diary [ENTRY]`: saves a diary entry.

Alternatively, you can save a note by prefacing a message with `Nn `. For example, you can send `Nn I like dogs` to save the note "I like dogs". You can also save a question-answer flashcard by just using the question-answer syntax i.e. `[QUESTION]??[ANSWER]`.

## Technicals

`helpivefallen` is a Telegram bot that runs on a DigitalOcean Droplet running Linux. My local repository of notes, flashcards, and diary entries are updated on a daily basis using a cronjob. Simple, but effective.

## Motivation

When I'm reading, I frequently look up definitions/concepts. However, Siri is usually terrible at understanding what I want, and doing a Google search means I have to parse through search results. This tool makes it easy for me to quickly look up a definition or a concept, and turn right back to my reading without interrupting my focus too heavily. 

I also jot down notes in the form of question-answers in a small notebook or in the book itself. But I usually get lazy and don't import the notes into my spaced repetition system. I have a horrible memory, so usually I'll have forgotten what I read a week or two later (provided that I stop thinking about it). This tool lets me avoid migrating notes every single time I'm learning/reading, and keeps my flashcards updated and ready-for-review. 