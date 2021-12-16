Welcome to Helix Starter Kit (Version 1.0)

Overview:

The hello world script for Helix is designed to be a starter kit for developers using Helix APIs to enhance their ability to customize and utilize the log data coming from their product into Helix. Version 1.0 of the script (which is the current version) allows you to only use the Helix search API to interact with your data. The Script can only be used with a valid API key. As This is an ever-expanding starter kit, please contact the script owner (Mahmoud.Eraqi@fireeye.com) if you have any questions or requests.

The script comes ready with the Helix MQL search API, which allows you to search all your data logs using MQL. Below you will see how to run the script and some overview/examples on how to use MQL.

Setting up Config file (config.ini):

    A user must be a Helix subscriber to gather the proper values to fill out the config file.

    Make sure to not change anything in the config file, but just fill out the blank values.

    All information can be gathered via your account admin and/or FireEye IAM portal.
    To obtain your api key, please visit the appropriate region url below.

    Config key description: 
        base_url: is the url for the endpoint
            US regions - https://apps.fireeye.com
            EU regions - https://helix.eu.fireeye.com
            AP regions - https://helix.ap.fireeye.com
        api_key: is API KEY (instructions below for how to obtain this key)
        helix_id: is the organization/instance id starting with "hex", found in the IAM portal (URL above)

    Here are steps to getting the API Key
        1. Login to FireEye's IAM portal for the region you're in and you're in the proper organization/instance, a list of the urls for each region below
            US regions - https://console.us.fireeye.com/console/settings/user
            EU regions - https://console.eu.fireeye.com/console/settings/user
            AP regions - https://console.ap.fireeye.com/console/settings/user 
        2. Navigate to API Keys tab in the left corner
        3. Navigate to "CREATE API KEY" Button in the right corner of the table
        4. Once there, follow the instructions:
            Select a unique name
            Select the Threat Analytics Platform
            Then, you will be able to give yourself the proper entitlements, which are permissions on what you can do in Helix such as making certain API calls and more.
            you MUST have "tap.search.browse" and "tap.search.regex" ENTITLEMENTS ENABLED.
        5. You should then see your API key, and options to copy it to clipboard, or download the text file.

Running the script:

    Run this command in the same directory as the helix_main.py:
        "python3 helix_main.py -q [run custom query]"
    This command will execute the file, here is an example when I try to run the script with MQL search parameter "has:class" (this can be changed as it’s a custom text)
        "python3 helix_main.py -q has:class"
    The "has:class" search will pull all data in the predefined time frame (which is 12hrs) into your custom csv file. Which you can also give it a unique name yourself as so:
        "python3 helix_main.py -q has:class -csv custom_file_name.csv"
        or if you don't specify the name it will default to: "helix_data_output[datetime stamp].csv"

    If you would like to see the other options or future options for the script, run the below command:
        "python3 helix_main.py -h"

Note: Some arguments are still in development.

Examples of MQL search (visit our developer hub portal for more documentations on MQL)

Here are a few examples of the syntax:

    1.class=test | groupby class
    2.!class=*.com
    3.srcport > 8999 and srcport < 9301
The use of pipes (|), wildcards (*), and operators (see below):

    The order of precedence for AND, OR, and NOT is:
        1. NOT, which binds to what immediately follows it
        2. AND (explicit)
        3. AND (implicit, or no AND is entered, but a space exists between two terms)
        4. OR
    The valid symbols for AND are:
         AND/and/&&/(single empty space)
    The valid symbols for OR are:
        OR/or/||
    The valid symbols for NOT are:
        NOT/Not/! (exclamation point with no space before next search term)

    Comparisons operators use/symbols:
        > rcvdpackets > 20
        < rcvdpackets < 20
        =< rcvdpackets <= 20
        >= rcvdpackets >= 20
Just like operators in Regular Expressions (RegEx) these operators can be used together and combined to make the most use out of creating your MQL search query.
