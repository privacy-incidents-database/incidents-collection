find . -name "*.txt" -print0 | xargs -0 sed -i '' -e 's/The\ New\ York\ Times//g'
find . -name "*.txt" -print0 | xargs -0 sed -i '' -e 's/NYTimes\.com no longer supports Internet Explorer 9 or earlier\. Please upgrade your browser\.//g'
find . -name "*.txt" -print0 | xargs -0 sed -i '' -e 's/Were interested in your feedback on this page\. Tell us what you think\.//g'
find . -name "*.txt" -print0 | xargs -0 sed -i '' -e 's/Accessibility concerns? Email us at accessibility\@nytimes\.com\. We would love to hear from you\.//g'
