#!/bin/python
# -*- coding: UTF-8 -*-

html = u"""
<html><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<!-- A minimal Flowplayer setup to get you started -->
  

	<!-- 
		include flowplayer JavaScript file that does  
		Flash embedding and provides the Flowplayer API.
	-->
	<script type="text/javascript" src="../flowplayer-3.1.0.min.js"></script>
	
	<!-- some minimal styling, can be removed -->
	<link rel="stylesheet" type="text/css" href="style.css">
	
	<!-- page title -->
	<title>%(title)s</title>

</head><body>

	<div id="page">
		
		<h1>%(title)s</h1>
	
		视频来源： <a href="www.wfbrood.com" target="_blank">www.wfbrood.com</a>  <br />
                整理 by ZelluX，如有相关建议或建议，请投条Zellux@日月光华BBS <br /><br />
		
		<!-- this A tag is where your Flowplayer will be placed. it can be anywhere -->
		<a  
			 href="0.flv"
			 style="display:block;width:480px;height:400px"  
			 id="player"> 
		</a> 

        <!-- this will install flowplayer inside previous A- tag. -->
        <script>
            flowplayer("player", "../flowplayer-3.1.0.swf", {
                playlist: [
%(playlist)s
                    ],
                clip:  { 
                    autoPlay: false, 
                    autoBuffering: true // last property, so remove this extra comma! 
                }
            });
		</script>
		
	</div>
	
	
</body></html>
"""
left = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
    <head>
        <title>right</title>
        <meta name="generator" content="Muse">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

        <link rel="stylesheet" type="text/css"charset="utf-8" media="all" href="styles.css"  />
    </head>

    <body>
        %s
    </body>
</html>

"""
