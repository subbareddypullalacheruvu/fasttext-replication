# Error analysis: ag_news_bigram

Test items: 7600; errors: 576

## Confusion matrix (rows = true, columns = predicted)

| true \ pred | World | Sports | Business | Sci/Tech | recall |
|---|---|---|---|---|---|
| **World** | 1752 | 39 | 64 | 45 | 92.2% |
| **Sports** | 19 | 1861 | 14 | 6 | 97.9% |
| **Business** | 55 | 12 | 1706 | 127 | 89.8% |
| **Sci/Tech** | 43 | 20 | 132 | 1705 | 89.7% |

## Examples from the three most common confusions

### Sci/Tech predicted as Business (132 cases)

- a distraction as a deadline approaches , as the holidays approach , christmas spirit is a bargain-hunting essential .
- microsoft settles antitrust cases with novell , ccia , microsoft corp on monday announced antitrust settlements with novell inc . and the computer and communica…
- supreme court asked to hear file-sharing arguments , the file-sharing legal battle has moved to the supreme court , with a group composed of labor unions , spor…
- nortel lowers expectations , nortel said it expects revenue for the third quarter to fall short of expectations .

### Business predicted as Sci/Tech (127 cases)

- hp to tempt holiday shoppers with sights and sounds , the computer-hardware giant , best known for products such as pcs and printers , on friday laid out its pl…
- is this the end of it as we know it ? , halsey minor , ceo of hosted integration provider grand central communications , has a powerful message for it in four y…
- let a thousand ideas flower china is a new hotbed of research , in recent years , hundreds of multinational companies have set up research laboratories in china…
- local group joins suit to de-list endangered species , bob briggs wifes family has owned about 1 , 000 acres of redwood forest off waddell creek since 1913 . he…

### World predicted as Business (64 cases)

- india ' s tata makes powerful debut , shares in indian software services giant tata consultancy close 16 higher on their market debut , raising \$1 . 2bn for th…
- oil prices bubble to record high , the price of oil has continued its sharp rise overnight , closing at a record high . the main contract in new york , light sw…
- \$78 , 000 for a cane that helped a legend walk the line , many of johnny cash ' s possessions were sold at sotheby ' s , collecting \$3 , 984 , 260 for the cas…
- expansion may lead to division , the asia-europe meeting , asem , will hold its fifth summit in hanoi in october amidst a recent crisis over the inclusion of my…
