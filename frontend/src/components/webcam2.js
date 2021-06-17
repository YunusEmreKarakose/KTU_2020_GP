// Import dependencies
import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import axios from 'axios'

function WebCamComp2() {
    const [xoffset, setX] = useState(0);
    const [yoffset, setY] = useState(0);
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
        //starting frame boxes   #252c37    
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
        //set video position with canvas
        let canvasElem = document.querySelector('canvas');
        let canvasRect = canvasElem.getBoundingClientRect();
        
        
        setX(xoffset+canvasRect.left)
        setY(yoffset+canvasRect.top)
        //mid point of canvas
        let cx=(canvasRect.left+canvasRect.right)/2
        let cy=(canvasRect.top+canvasRect.bottom)/2
        //send req         
        const requestTimer=3000;
        setInterval(() => {
            if(
                typeof webcamRef.current !== "undefined" &&
                webcamRef.current !== null &&
                webcamRef.current.video.readyState === 4
              )
              {
                //base64 image
                var imageSrc=webcamRef.current.getScreenshot({width: 1280, height: 720});
                //remove "data:image/jpeg;base64,"
                imageSrc=imageSrc.replace('data:image/jpeg;base64,','');
                //send request            
                const fd=new FormData();
                fd.append('b64image',imageSrc)
                const url='http://localhost:8000/webcamFD/'
                
                axios.post(url,fd)
                .then((response)=>{
                    
                    //update frame boxes
                    if(typeof response.data.left!=="undefined" && typeof response.data.upper!=="undefined"){
                        //console.log("left-upper:::"+response.data.left+" | "+response.data.upper)
                        //console.log("right-lower:::"+response.data.right+" | "+response.data.lower)
                        //if B=(x,y) middle of blob and capture size mxn
                        var x=(response.data.left+response.data.right)/2;
                        var y=(response.data.upper+response.data.lower)/2;
                        // |x-cx|<320 
                        if((x-cx)<0 && Math.abs(x-cx)<160){
                            console.log("if 22222::::::"+xoffset)
                            const processTimer=100;
                            const step=(requestTimer/2)/processTimer;
                            var i=0;
                            var process=setInterval(()=>{
                                                              
                                setX(xoffset=>xoffset+160/step)
                                i++;	
                                 if(i>=step){  
                                   clearInterval(process);
                                 }
                             },processTimer);
                            //setX(xoffset+320)
                        }else {
                            const processTimer=100;
                            const step=(requestTimer/2)/processTimer;
                            var i=0;
                            var process=setInterval(()=>{
                                                              
                                setX(xoffset=>xoffset-160/step)
                                i++;	
                                 if(i>=step){  
                                   clearInterval(process);
                                 }
                             },processTimer);
                            //setX(xoffset)
                            console.log("if 33333::::"+xoffset)
                        }
                        //|y-cy|<180
                        
                    }    
                }).catch(err=>{
                    console.log(err)
                })
              }
          }, requestTimer);
    }
    useEffect(()=>{sendReq()}, []);
    const moveTitleToDown = () => {
        console.log(yoffset)
        setY(yoffset-20);
    };
    const moveTitleToRight = () => {
        console.log(xoffset)
        setX(xoffset+20);
    };
    const moveTitleToLeft = () => {
        /*
        const processTimer=100;
        var i=0;
        var process=setInterval(()=>{                                
            setX(xoffset=>xoffset-20)
            console.log(xoffset)
            i++;	
            if(i>=10){  
                clearInterval(process);
            }
            },processTimer);*/
        setX(xoffset-20);
    };
    const moveTitleToUp = () => {
        setY(yoffset+20);
    };

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
                    style={{
                        position: "absolute",
                        left: `${xoffset}px`,
                        top: `${yoffset}px`,
                      }}
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
                <div style={{ marginTop: "500px" }}>
                    <button onClick={moveTitleToRight}>
                        Move Title To Right
                    </button>
                    <button onClick={moveTitleToDown}>
                        Move Title To Down
                    </button>
                    <button onClick={moveTitleToLeft}>
                        Move Title To Left
                    </button>
                    <button onClick={moveTitleToUp}>
                        Move Title To Up
                    </button>
                </div>
            </header>
        </div>
    );
}

export default WebCamComp2;