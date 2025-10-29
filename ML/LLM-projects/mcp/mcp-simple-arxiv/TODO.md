# Planned Features and Improvements

1. **Total Match Count in Search Results**
   - Add total number of matches found to search results
   - This helps users and AIs determine if search needs refinement
   - Should handle cases where there are more results than displayed
   - Example: "Found 1234 matches, showing first 10"

2. **Categories in Search Results**
   - Show primary category and all subcategories for each paper in search results
   - Makes it easier to quickly assess paper's field and relevance
   - Categories should be clearly labeled (primary vs additional)
   - Example: "Primary: cs.AI, Additional: cs.LG, cs.CL"

3. **Abstract Preview in Search Results**
   - Add first 2-3 sentences of abstract to each search result
   - Helps quickly assess paper relevance without fetching full details
   - Should handle varying abstract lengths gracefully
   - Should end with ellipsis (...) if truncated

4. **Flexible Search Result Sorting**
   - Add support for different sorting options in search
   - Support sorting by: submission date, last update date, relevance
   - Make sort order configurable (ascending/descending)
   - Expose sorting options in tool description

5. **Date Range Filters**
   - Allow filtering papers by submission/update date range
   - Support both absolute dates and relative ranges (last week/month/year)
   - Implement using arXiv API's date filtering capabilities

6. **DOI Integration** [DONE]
   - Add DOI (Digital Object Identifier) to paper details when available
   - Extract from arXiv API response
   - Include DOI URL for easy access

7. **Enhanced Category Presentation**
   - Improve how categories are displayed in paper details
   - Clearly distinguish primary and secondary categories
   - Include category descriptions where helpful
   - Group related categories together

8. **Advanced Category Search**
   - Support complex category combinations in search
   - Allow AND/OR/NOT operations between categories
   - Support parentheses for grouping
   - Example: "(cs.AI OR cs.LG) AND NOT cs.DB"

9. **Citation Format Support**
   - Generate citation strings in common formats (BibTeX, APA, etc.)
   - Include all necessary metadata (authors, title, arXiv ID, etc.)
   - Handle special characters in titles and names correctly

10. **Impact Metrics**
    - Add citation count or other impact metrics if available
    - Consider alternative metrics like downloads or social media mentions
    - NOTE: Might require integration with additional APIs

11. **HTML Paper Access**  [DONE]
    - Add detection of HTML version availability
    - Include HTML URL in paper metadata when available
    - Add URL construction logic (changing PDF URL to HTML)