% include('header.tpl', title='LSD Dimensions')

<h2>Details for dimension {{dim}}</h2>

<h3>Endpoints with dimension {{dim}}</h3>
  %for endpoint in endpoints["result"]:
  %    ep = endpoint["_id"]
  <p>{{ep}}</p>
  %end

<h3>Popular codes associated with dimension {{dim}}</h3>
  %for code in codes["result"]:
  %    code_uri = code["_id"]["uri"]
  %    code_label = code["_id"]["label"]
  <p>{{code_uri}}, {{code_label}}</p>
  %end

<a href="/dimensions">Back</a>

% include('footer.tpl')
