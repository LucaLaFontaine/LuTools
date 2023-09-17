import pandas as pd
import numpy as np

def get100LowestValues(df, minVal=1):
    """
Gets the 100 lowest values from each column provided in df
It will filter anything lower than minVal, so it'll ignore negative or blank values if minVal=1

Parameters:
df: DataFrame, required
minVal: int, default: 1  

Returns: DataFrame
    """    
    colList = []
    for col in df.columns:
        colSeries = df.loc[df[col] >= minVal, col].sort_values().head(100)
        colList.append(colSeries)

    df  = pd.concat(colList, axis=1)   
    return df

def getNRowAvg(df, rows, ascending):
    # should be a series
    return round(df.sort_values(ascending=ascending).reset_index().loc[:rows].mean())

def gapAndIsland(dfCol):
    """Should be renamed to gapAndIsland
    takes an np.series data type (ie. a df single column)
    returns the entire column broken up into sections where all the numbers are the same. 
    Good for iterating on an events column or tracking flags. 

    new: dfCol can be df with one column or series
    """
    return np.split(dfCol.squeeze(), np.where(np.diff(dfCol.squeeze()) != 0)[0]+1)

def mergeCloseEvents(events, mergeWithinHours=12, i=1):
    """Merges events that are close so we don't get bunches of events. Not entirely necessary but it makes it cleaner. 
    Recursive function, so it takes each event and calculates if it's within 3600sec of the last event. 
    If so it adds this event to the last event and deletes this event.
    returns the new list of events
    """
    if i >= len(events):
        return events
    
    eventStart = events[i][0]
    eventEnd = events[i][-1]
    lastEventEnd = events[i-1][-1]

    if ((eventStart-lastEventEnd).total_seconds()/3600)<=mergeWithinHours:
        lastEventEnd = eventEnd
        events.pop(i)
        events = mergeCloseEvents(events, i = i)
        
    else:
        mergeCloseEvents(events, i=i+1)
    return events

def extendTags(tags,  maxNum, exampleNum=1, missing=[],):
    """
    Use to extend a list of tags (usually tags in an EMS or files) for one grouping into many
    Say you have 5 tags each for 10 AHUs that you have to pull. Use this to generate all 50 tags from the first 5

    Parameters:
    tags: list, Required
    maxNum: int, Required, largest number in the set
    exampleNum: int, Default: 1, number you're replacing in the exmple set
    missing: list, Default: empty, any missing numbers in the set
    """
    extendedTags = []
    for i in range(1, maxNum+1):
        for j, tag in enumerate(tags):
            if i in missing:
                continue
            if tag.find(str(i)):
                extendedTags.append(tag.replace(str(exampleNum), str(i)))     
    return extendedTags