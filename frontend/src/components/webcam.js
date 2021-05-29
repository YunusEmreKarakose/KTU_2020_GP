// Import dependencies
import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import axios from 'axios'
// 2. TODO - Import drawing utility here
// e.g. import { drawRect } from "./utilities";

function WebCamComp() {
    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user"
    };
    
    const webcamRef = React.useRef(null);
    const canvasRef = useRef(null);
    const sendReq=()=>{
        //Draw frame boxes        
        canvasRef.current.width = 1280;
        canvasRef.current.height = 720;
        const ctx = canvasRef.current.getContext("2d");       
        // A=(c,r) is referance point
        var Ac=320;
        var Ar=180;
        //starting frame boxes       
        ctx.beginPath();
        ctx.strokeStyle = "red";        
        ctx.lineWidth = "4";
        ctx.rect(Ac, Ar, 640, 360);
        ctx.stroke();
        //box1 0,0, 1280, Ar        
        ctx.beginPath();
        ctx.strokeStyle = "blue";   
        ctx.lineWidth = "8";
        ctx.rect(0, 0, 1280, Ar);
        ctx.stroke();
        //box2 0,Ac,Ar,360    
        ctx.beginPath();
        ctx.strokeStyle = "yellow";  
        ctx.lineWidth = "8";
        ctx.rect(0, Ar, Ac, 360);
        ctx.stroke();
        //box3 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "green"; 
        ctx.lineWidth = "8";
        ctx.rect(Ac+640, Ar, Ac, 360);
        ctx.stroke();        
        //box4 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "purple";
        ctx.lineWidth = "8";
        ctx.rect(0, Ar+360, 1280, 360);
        ctx.stroke(); 
        //send req 
        setInterval(() => {
            if(
                typeof webcamRef.current !== "undefined" &&
                webcamRef.current !== null &&
                webcamRef.current.video.readyState === 4
              )
              {
                //base64 image
                var imageSrc=webcamRef.current.getScreenshot();
                //remove "data:image/jpeg;base64,"
                imageSrc=imageSrc.replace('data:image/jpeg;base64,','');
                //send request            
                const fd=new FormData();
                fd.append('b64image',imageSrc)
                const url='http://localhost:8000/webcamFD/'
                
                axios.post(url,fd)
                .then((response)=>{
                    // Set canvas height and width
                    canvasRef.current.width = 640;
                    canvasRef.current.height = 360;
                    const ctx = canvasRef.current.getContext("2d");
                    // Draw blob rectangle
                    ctx.beginPath();   
                    var boxWidth=response.data.right-response.data.left;
                    var boxHeight=response.data.lower-response.data.upper;
                    ctx.lineWidth = "6";                    
                    ctx.strokeStyle = "red";
                    ctx.rect(response.data.left,response.data.upper, boxWidth,boxHeight ); 
                    ctx.stroke();
                    //update frame boxes
                    if(typeof response.data.left!=="undefined" && typeof response.data.upper!=="undefined"){
                        Ac=response.data.left
                        Ar=response.data.upper
                    }
                    console.log(response.data.left+"  "+response.data.upper)
                    //b1                  252c37    
                    ctx.beginPath();
                    ctx.strokeStyle = "blue";
                    ctx.lineWidth = "4";
                    ctx.rect(0, 0, 640, Ar/2);
                    ctx.stroke();
                    //b2                   
                    ctx.beginPath();
                    ctx.strokeStyle = "yellow";
                    ctx.lineWidth = "4";
                    ctx.rect(0, Ar/2, Ac/2, 180);
                    ctx.stroke();
                    //b3   
                    ctx.beginPath();
                    ctx.strokeStyle = "green";
                    ctx.lineWidth = "4";
                    ctx.rect((Ac+640)/2, Ar/2, 320-Ac/2, 180);
                    ctx.stroke();        
                    //b4
                    ctx.beginPath();
                    ctx.strokeStyle = "purple";
                    ctx.lineWidth = "4";
                    ctx.rect(0, (Ar+360)/2, 720, 180);
                    ctx.stroke(); 
    
                }).catch(err=>{
                    console.log(err)
                })
              }
          }, 500);
    }
    useEffect(()=>{sendReq()},[]);
    return (
        <div className="WebcamApp">
            <header className="App-header">
                <Webcam
                    audio={false}
                    height={360}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width={640}
                    videoConstraints={videoConstraints}
                />
                <canvas
                    ref={canvasRef}
                    style={{
                        position: "absolute",
                        marginLeft: "auto",
                        marginRight: "auto",
                        left: 0,
                        right: 0,
                        textAlign: "center",
                        zindex: 8,
                        width: 640,
                        height: 360,
                    }}
                />
            </header>
        </div>
    );
}

export default WebCamComp;