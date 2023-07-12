import React from 'react';

import ResultListItem from './ResultListItem';

function ResultList ({ results }){
    return (
      <div>
        {!results && <p>Search using the left panel.</p>}
        {results && results.length === 0 && <p>No results found.</p>}
        {results.map(result =>  <ResultListItem key={result.id} result={result} />)}
      </div>
    );
}

export default ResultList;