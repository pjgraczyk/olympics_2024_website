param(
    [string]$InputFile,
    [string]$OutputFile1,
    [string]$OutputFile2,
    [double]$SplitRatio = 0.5
)

function Split-CsvFile {
    param(
        [string]$InputFile,
        [string]$OutputFile1,
        [string]$OutputFile2,
        [double]$SplitRatio
    )

    # Read the CSV file
    $csvData = Import-Csv -Path $InputFile

    # Calculate the split index
    $splitIndex = [math]::Ceiling($csvData.Count * $SplitRatio)

    # Split the data
    $part1 = $csvData | Select-Object -First $splitIndex
    $part2 = $csvData | Select-Object -Skip $splitIndex

    # Export the split data to new CSV files
    $part1 | Export-Csv -Path $OutputFile1 -NoTypeInformation
    $part2 | Export-Csv -Path $OutputFile2 -NoTypeInformation

    Write-Host "CSV file has been split into two parts:"
    Write-Host "Part 1: $OutputFile1"
    Write-Host "Part 2: $OutputFile2"
}

# Example usage
Split-CsvFile -InputFile "data/athlete_events.csv" -OutputFile1 "output1.csv" -OutputFile2 "output2.csv" -SplitRatio 0.5