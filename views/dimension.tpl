% include('header.tpl', title='LSD Dimensions')

<h2>Details for dimension <a href="{{dim}}" target="_blank">{{dim}}</a></h2>

<div class="container">
<dl class="dl-horizontal">
<dt>Endpoints</dt>
  %for endpoint in endpoints:
  %    ep = endpoint
  <dd><a href="{{ep}}" target="_blank">{{ep}}</a></dd>
  %end
  %if not endpoints:
  <dd>N/A</dd>
  %end

<dt>Codes</dt>
  %for code in codes["result"]:
  %    code_uri = code["_id"]["uri"]
  %    code_label = code["_id"]["label"]
  <dd><a href="{{code_uri}}" target="_blank">{{code_uri}}</a>, {{code_label}}</dd>
  %end
  %if not codes["result"]:
  <dd>N/A</dd>
  %end
</dl>
</div>

<a href="/dimensions">Back</a>

% include('footer.tpl')
