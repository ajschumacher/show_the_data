# show the data


### variables of interest

 * "PWGTP: Person weight for generating statistics on individuals (such as age)."
     * WGTP: the housing (household) ones
 * ADJINC: "Divide ADJINC by 1,000,000 to obtain the inflation adjustment factor and multiply it to the PUMS variable value to adjust it to 2024 dollars."
 * AGEP: age, top-coded at 99
 * PINCP: "Total person's income (use ADJINC to adjust to constant dollars)"
    * -19997:-1: Loss $1 to $19997 (Rounded components)
    * -19998: Loss of $19998 or more (Rounded and bottom- coded components)
    * -19999: N/A (less than 15 years old). Unselect this value to get correct calculation of average for this variable
    * 0: None
    * 1:4209995: $1 to $4209995 (Rounded and top-coded components)
 * HINCP is the household income one...
 * OCCP: "Occupation recode for 2018 and later based on 2018 OCC codes"
 * SOCP: "Standard Occupational Classification (SOC) codes for 2018 and later based on 2018 SOC codes"
    * these ones have possibly handy three-letter groups like "EDU"...


### data files

```bash
# https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip
md5 csv_pus.zip
# MD5 (csv_pus.zip) = cf49a71f579984f6bba5d64dfd27af98
unzip csv_pus.zip
# Archive:  csv_pus.zip
#   inflating: psam_pusa.csv
#   inflating: psam_pusb.csv
#   inflating: ACS2024_PUMS_README.pdf
awk -F',' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i} {print $h["PWGTP"] "," $h["ADJINC"] "," $h["AGEP"] "," $h["PINCP"] "," $h["OCCP"] "," $h["SOCP"]}' psam_pusa.csv > smallera.csv
awk -F',' 'NR==1{for(i=1;i<=NF;i++) h[$i]=i} {print $h["PWGTP"] "," $h["ADJINC"] "," $h["AGEP"] "," $h["PINCP"] "," $h["OCCP"] "," $h["SOCP"]}' psam_pusb.csv > smallerb.csv
{ cat smallera.csv; tail -n +2 smallerb.csv; } > smaller.csv
rm smaller?.csv

# okay can we make this better?
curl -O https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_hus.zip
unzip csv_hus.zip
csvstack psam_husa.csv psam_husb.csv | csvcut -c WGTP,ADJINC,HINCP > 2024h.csv
```


### env

```bash
pyenv install 3.14.3
pyenv virtualenv 3.14.3 show_the_data
pyenv local show_the_data
pip install jupyter matplotlib pandas
pip install csvkit  # but then I used awk etc...
  # ah, I'm using it now!
pip install statsmodels
pip freeze > requirements.txt
```


### references

 * https://github.com/30DayChartChallenge/Edition2026/blob/main/list_prompts.md
 * https://perthirtysix.com/essay/30-day-chart-challenge-2024
 * https://www.bls.gov/soc/2018/major_groups.htm SOC code groups
     * edu ones start with "25"
 * https://github.com/ajschumacher/income
 * https://planspace.org/20220702-what_are_people_doing/
 * https://planspace.org/20220703-common_jobs_by_income_range/
