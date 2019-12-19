Set-StrictMode -Version 3

$Output = (netsh wlan show profiles)

[System.Collections.ArrayList] $ProfileNames = @()
[System.Collections.ArrayList] $Results = @()

ForEach ($Line in $Output)
{
    $Line = $Line -Match 'All User Profile\s+:\s+(.+)$'
    
    If ($Line) {
        $ProfileNames.Add($Matches.Item(1)) > $Null
    }
}

ForEach ($ProfileName In $ProfileNames)
{
    $Output = (netsh wlan show profile name="$ProfileName" key=clear)
    
    ForEach ($Line In $Output) {
        $Line = $Line -Match 'Key Content\s+:\s+(.+)$'

        If ($Line) {
            $Password = ${Matches}.Item(1)
            $Results.Add(@{"${ProfileName}"="${Password}"}) > $Null
            Break
        }

    }
}

Write-Output $Results
