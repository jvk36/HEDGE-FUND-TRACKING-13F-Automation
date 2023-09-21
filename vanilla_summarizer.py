from transformers import pipeline

summarizer = pipeline("summarization") # , model="facebook/bart-large-cnn")

# NOTE: The hedge fund articles usually exceed the 1024 token limit for both the default 
# sshleifer/distilbart-cnn-12-6 model as well as the facebook/bart-large-cnn . So, the input
# should be truncated. In the below text, the article text was truncated after the "Stake Disposals:" para.
print(summarizer(
    """
This article is part of a series that provides an ongoing analysis of the changes made to David Einhorn’s Greenlight Capital 13F portfolio on a quarterly basis. It is based on Einhorn’s regulatory 13F Form filed on 8/14/2023. Please visit our Tracking David Einhorn's Greenlight Capital Holdings article series for an idea on his investment philosophy and our previous update for the fund’s moves during Q1 2023. 

Greenlight Capital’s 13F portfolio value stood at $2.13B this quarter. It is up ~16% compared to $1.84B as of last quarter. Einhorn’s Q2 2023 letter reported that the fund returned 14.5% for Q2 2023 vs 8.7% for the S&P 500 Index.  Since 1996 inception, Greenlight has returned ~12.6% annualized vs 9.1% annualized for S&P 500 index. In addition to partner stakes, the fund also invests the float of Greenlight Capital RE (GLRE). To learn about David Einhorn and the perils of shorting, check-out his “Fooling Some of the People All of the Time, A Long Short (and Now Complete) Story”.


New Stakes:


Net Power Inc. (NPWR): NPWR is a 1.53% of the portfolio position purchased this quarter at a cost-basis of $10.10 per share. The stock currently trades at $15.58. 

Activision Blizzard (ATVI), First Horizon Corp (FHC), and Seadrill Ltd. (SDRL): These are very small (less than ~1% of the portfolio each) new stakes established this quarter. 


Stake Disposals:


Global Payments (GPN): GPN was a 3.43% of the portfolio stake. It was established in Q4 2021 at prices between ~$118 and ~$161. Q3 2022 saw the stake sold down by ~47% at prices between ~$108 and ~$137. There was a ~120% stake increase in the last two quarters at prices between ~$93 and ~$125. The disposal this quarter was at prices between ~$96 and ~$113. The stock is now at ~$126. 

Note: Greenlight’s Q2 2023 letter mentioned a ~6% IRR on this holding. They exited as they were uncomfortable with the company’s increasingly large adjustments to reported numbers and an abrupt CEO change. 

Civitas Resources (CIVI): The 1.70% CIVI stake saw a roughly two-thirds increase during Q4 2022 at prices between ~$56 and ~$71 and it is now at $85.24. The position was sold this quarter at prices between ~$65 and ~$74.  

Note: The investment had a ~35% IRR. The stake came about through purchasing distressed debt of Extraction Oil & Gas before it’s bankruptcy in June 2020. 

Concentrix Corp (CNXC): The small 1.37% CNXC position saw a ~150% stake increase during Q3 2022 at prices between ~$110 and ~$137. That was followed with a ~115% increase this quarter at prices between ~$118 and ~$151. The disposal this quarter was at prices between ~$81 and ~$122. The stock currently trades at ~$72. 

"""
))
