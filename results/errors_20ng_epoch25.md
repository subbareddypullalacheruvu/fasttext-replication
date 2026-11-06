# Error analysis: 20ng_epoch25

Test items: 2190; errors: 824

## Confusion matrix (rows = true, columns = predicted)

| true \ pred | alt_atheism | comp_graphics | comp_os_ms-windows_misc | comp_sys_ibm_pc_hardware | comp_sys_mac_hardware | comp_windows_x | misc_forsale | rec_autos | rec_motorcycles | rec_sport_baseball | rec_sport_hockey | sci_crypt | sci_electronics | sci_med | sci_space | soc_religion_christian | talk_politics_guns | talk_politics_mideast | talk_politics_misc | talk_religion_misc | recall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **alt_atheism** | 53 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 3 | 1 | 2 | 1 | 8 | 6 | 3 | 6 | 5 | 57.0% |
| **comp_graphics** | 0 | 70 | 8 | 7 | 1 | 7 | 1 | 2 | 1 | 1 | 0 | 1 | 8 | 3 | 2 | 0 | 1 | 0 | 0 | 0 | 61.9% |
| **comp_os_ms-windows_misc** | 0 | 10 | 70 | 14 | 4 | 8 | 1 | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 61.9% |
| **comp_sys_ibm_pc_hardware** | 0 | 4 | 10 | 66 | 10 | 4 | 6 | 1 | 1 | 0 | 0 | 1 | 9 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 56.9% |
| **comp_sys_mac_hardware** | 0 | 4 | 4 | 20 | 54 | 4 | 2 | 5 | 5 | 0 | 0 | 1 | 11 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 48.6% |
| **comp_windows_x** | 1 | 18 | 5 | 1 | 1 | 80 | 1 | 0 | 0 | 1 | 0 | 1 | 4 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 68.4% |
| **misc_forsale** | 0 | 2 | 2 | 10 | 0 | 0 | 82 | 5 | 2 | 0 | 2 | 1 | 5 | 1 | 1 | 0 | 0 | 0 | 2 | 0 | 71.3% |
| **rec_autos** | 0 | 0 | 0 | 2 | 3 | 2 | 1 | 66 | 18 | 2 | 2 | 0 | 6 | 1 | 2 | 0 | 3 | 1 | 1 | 1 | 59.5% |
| **rec_motorcycles** | 4 | 3 | 2 | 0 | 1 | 0 | 2 | 9 | 73 | 0 | 1 | 0 | 0 | 2 | 3 | 1 | 13 | 1 | 1 | 0 | 62.9% |
| **rec_sport_baseball** | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 3 | 11 | 75 | 10 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 66.4% |
| **rec_sport_hockey** | 0 | 0 | 1 | 1 | 1 | 0 | 2 | 0 | 3 | 14 | 83 | 0 | 1 | 0 | 2 | 1 | 3 | 3 | 1 | 0 | 71.6% |
| **sci_crypt** | 0 | 0 | 1 | 0 | 0 | 2 | 1 | 1 | 1 | 0 | 0 | 85 | 5 | 4 | 2 | 0 | 9 | 0 | 5 | 0 | 73.3% |
| **sci_electronics** | 1 | 2 | 3 | 8 | 7 | 0 | 1 | 9 | 3 | 0 | 1 | 0 | 66 | 3 | 9 | 0 | 1 | 0 | 0 | 1 | 57.4% |
| **sci_med** | 2 | 7 | 1 | 0 | 0 | 0 | 0 | 2 | 3 | 1 | 2 | 2 | 2 | 87 | 0 | 1 | 2 | 0 | 2 | 1 | 75.7% |
| **sci_space** | 1 | 0 | 2 | 1 | 1 | 1 | 1 | 1 | 4 | 0 | 0 | 4 | 8 | 5 | 77 | 0 | 6 | 1 | 2 | 0 | 67.0% |
| **soc_religion_christian** | 6 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 1 | 5 | 1 | 85 | 6 | 1 | 1 | 7 | 72.0% |
| **talk_politics_guns** | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 1 | 2 | 5 | 3 | 1 | 3 | 3 | 67 | 1 | 10 | 2 | 63.2% |
| **talk_politics_mideast** | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 5 | 1 | 1 | 2 | 1 | 0 | 6 | 7 | 10 | 68 | 3 | 3 | 62.4% |
| **talk_politics_misc** | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 6 | 1 | 1 | 4 | 2 | 14 | 5 | 48 | 2 | 53.3% |
| **talk_religion_misc** | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 1 | 0 | 2 | 2 | 1 | 22 | 5 | 4 | 5 | 11 | 15.3% |

## Examples from the three most common confusions

### talk_religion_misc predicted as soc_religion_christian (22 cases)

- i will clarify my earlier quote . god ' s laws were originally written for the israelites . jesus changed that fact by now making the law applicable to all peop…
- ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ when are we going to hear a chris…
- the primary problem in human nature is a fragmentation of being . humans are in a state of tension , a tension of opposites . good and evil are the most thought…
- i understand and sympathize with your pain . what happened in waco was a very sad tradgedy . don ' t take it out on us christians though . the branch davidians …

### comp_sys_mac_hardware predicted as comp_sys_ibm_pc_hardware (20 cases)

- hm , i ' ve got my cd drive since 921230 . indeed , cds are bundled with it . you usually get nine cds with demos of applications , games , photos , etc . i hav…
- i seem to be having some trouble with this . . . i can get the mac to go to sleep , but i can ' t make seem to make it wake up with setwutime ( ) . i am aware o…
- the kit is for an already existing laserwriter iintx . it is a rom upgrade that replaces the font rasterizer code with the more efficient , speedier code that f…
- the real question here in my opinion is what motorola processors running system 7 on a mac are comparable to what intel processors running windows on a pc ? i r…

### comp_windows_x predicted as comp_graphics (18 cases)

- <i might have a need in the future to display rotated text . i noticed the <xvertext package on the net . it looks very good , but it has one slight <problem . …
- the following packages meet your criteria in that they are pd and present an aesthetically pleasant graphical interface to the users . if you can use 386bsd the…
- hi , iam looking for information on any work that deals with real-time support in x-windows ? ? ? ? ! ! would be happy if you could provide any pointers or info…
- it ' s the unix domain socket ( local connection ) to your xserver . try to rm it )
