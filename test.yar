

rule MSIETabularActivex
{
        meta:
                ref = "CVE-2010-0805"
                impact = 7
                hide = true
                author = "@d3t0n4t0r"
        strings:
                $cve20100805_1 = pp
                $cve20100805_2 = "DataURL" nocase fullword
                $cve20100805_3 = "true"
        condition:
                ($cve20100805_1 and $cve20100805_3) or (all of them)
}
