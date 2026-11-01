# Error analysis: 20ng_epoch25

Test items: 2190; errors: 814

## Confusion matrix (rows = true, columns = predicted)

| true \ pred | alt_atheism | comp_graphics | comp_os_ms-windows_misc | comp_sys_ibm_pc_hardware | comp_sys_mac_hardware | comp_windows_x | misc_forsale | rec_autos | rec_motorcycles | rec_sport_baseball | rec_sport_hockey | sci_crypt | sci_electronics | sci_med | sci_space | soc_religion_christian | talk_politics_guns | talk_politics_mideast | talk_politics_misc | talk_religion_misc | recall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **alt_atheism** | 56 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 3 | 1 | 3 | 1 | 7 | 5 | 2 | 7 | 4 | 60.2% |
| **comp_graphics** | 0 | 72 | 7 | 7 | 1 | 7 | 1 | 2 | 1 | 1 | 0 | 1 | 7 | 3 | 2 | 0 | 1 | 0 | 0 | 0 | 63.7% |
| **comp_os_ms-windows_misc** | 0 | 10 | 72 | 13 | 4 | 7 | 1 | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 63.7% |
| **comp_sys_ibm_pc_hardware** | 0 | 4 | 10 | 64 | 12 | 4 | 6 | 1 | 1 | 0 | 0 | 1 | 9 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 55.2% |
| **comp_sys_mac_hardware** | 0 | 5 | 4 | 22 | 53 | 3 | 3 | 5 | 4 | 0 | 0 | 1 | 10 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 47.7% |
| **comp_windows_x** | 1 | 17 | 5 | 1 | 1 | 80 | 1 | 0 | 0 | 1 | 0 | 1 | 5 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 68.4% |
| **misc_forsale** | 0 | 3 | 2 | 8 | 0 | 0 | 82 | 5 | 2 | 1 | 2 | 1 | 5 | 1 | 1 | 0 | 0 | 0 | 2 | 0 | 71.3% |
| **rec_autos** | 0 | 0 | 0 | 2 | 3 | 2 | 1 | 67 | 18 | 2 | 1 | 0 | 6 | 1 | 1 | 0 | 3 | 2 | 1 | 1 | 60.4% |
| **rec_motorcycles** | 3 | 3 | 2 | 0 | 1 | 0 | 2 | 9 | 71 | 0 | 2 | 0 | 0 | 3 | 2 | 1 | 14 | 1 | 2 | 0 | 61.2% |
| **rec_sport_baseball** | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 4 | 11 | 77 | 8 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 5 | 0 | 68.1% |
| **rec_sport_hockey** | 0 | 0 | 1 | 1 | 1 | 0 | 2 | 1 | 3 | 13 | 84 | 0 | 0 | 0 | 2 | 1 | 3 | 3 | 1 | 0 | 72.4% |
| **sci_crypt** | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 0 | 86 | 5 | 4 | 2 | 0 | 9 | 0 | 5 | 0 | 74.1% |
| **sci_electronics** | 1 | 5 | 3 | 6 | 6 | 0 | 1 | 9 | 3 | 0 | 1 | 0 | 66 | 3 | 8 | 0 | 1 | 1 | 0 | 1 | 57.4% |
| **sci_med** | 1 | 7 | 1 | 0 | 1 | 0 | 0 | 1 | 4 | 1 | 2 | 2 | 2 | 87 | 0 | 1 | 2 | 0 | 2 | 1 | 75.7% |
| **sci_space** | 1 | 1 | 2 | 0 | 1 | 1 | 1 | 1 | 4 | 0 | 0 | 4 | 8 | 4 | 78 | 0 | 6 | 1 | 2 | 0 | 67.8% |
| **soc_religion_christian** | 6 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 5 | 1 | 86 | 6 | 0 | 1 | 7 | 72.9% |
| **talk_politics_guns** | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 0 | 3 | 5 | 3 | 1 | 3 | 3 | 67 | 0 | 11 | 2 | 63.2% |
| **talk_politics_mideast** | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 4 | 1 | 1 | 2 | 1 | 1 | 4 | 7 | 11 | 69 | 2 | 3 | 63.3% |
| **talk_politics_misc** | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 7 | 1 | 1 | 4 | 2 | 15 | 5 | 48 | 2 | 53.3% |
| **talk_religion_misc** | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 1 | 0 | 2 | 2 | 1 | 23 | 5 | 4 | 5 | 11 | 15.3% |

## Examples from the three most common confusions

### talk_religion_misc predicted as soc_religion_christian (23 cases)

- [ . . . dr . england ' s story deleted , it was a nice read the first time through . . . ]] it isn ' t so much a matter of ' interpretation ' of bible texts tha…
- i will clarify my earlier quote . god ' s laws were originally written for the israelites . jesus changed that fact by now making the law applicable to all peop…
- the primary problem in human nature is a fragmentation of being . humans are in a state of tension , a tension of opposites . good and evil are the most thought…
- >based on the amount of e-mail from fellow christians who have read the >posts and told me i was wasting my time with butler and joslin , i told >them i wasn ' …

### comp_sys_mac_hardware predicted as comp_sys_ibm_pc_hardware (22 cases)

- i seem to be having some trouble with this . . . i can get the mac to go to sleep , but i can ' t make seem to make it wake up with setwutime ( ) . i am aware o…
- i just read an article on the swii . one thing puzzles me the article says the swii is a serial-only device . does that mean i ' ll have to unplug my modem each…
- as of last week , mac ' s place had the applied engineering quicksilver card ( 32k cache , one pds slot , socket for fpu ) on sale for $99 . 00 ( without fpu ) …
- a couple of questions for the multimedia set 1 . does anybody have a phone or fax number , or e-mail address , or name of a principal in cedar technologies in d…

### rec_autos predicted as rec_motorcycles (18 cases)

- ^^^^ rears also vented then you shouldn ' t ' ve done it . try answering the damn question . i am well aware of the fact that there was no mention of the sc in …
- geez wharfie , do you have to be so difficult ? mine was built in december ' 88 , which qualifies as pretty dang early , and it most certainly grinds away .
- well , before we start calling the engineering folks in france a bunch of braindeads for this . . . my 1979 mercury capri had this lovely feature . this was not…
- hm . . . i find this hard to believe . v16t weights about the same as the red head , but it has hell lot more horse power . perhaps it ' s due to pre-production…
