// Import dependencies
import React from "react";
import Webcam from "react-webcam";
import axios from 'axios'

class WebCamComp4 extends React.Component {
    // Create state
    state = {
        xoffset: 0,
        yoffset: 0,
        canLe:0,//canvas left
        canTo:0,//canvas top
        canWi:0,//width
        canHe:0,//height
    };
    //setref webcam
    webcamRef = webcam => {
        this.webcam = webcam;
    };
    canvasRef= React.createRef();
    
    componentDidMount() {
        //Draw frame boxes        
        this.canvasRef.current.width = 1280;
        this.canvasRef.current.height = 720;
        const canvas = this.canvasRef.current;
        const ctx = canvas.getContext('2d');
        // A=(c,r) is referance point
        var Ac=320;
        var Ar=180;
        //starting frame boxes   #252c37    
        //box1 0,0, 1280, Ar        
        ctx.beginPath();
        ctx.strokeStyle = "red";   
        ctx.lineWidth = "8";
        ctx.rect(0, 0, 1280, Ar);
        ctx.stroke();
        //box2 0,Ac,Ar,360    
        ctx.beginPath();
        ctx.strokeStyle = "red";  
        ctx.lineWidth = "8";
        ctx.rect(0, Ar, Ac, 360);
        ctx.stroke();
        //box3 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "red"; 
        ctx.lineWidth = "8";
        ctx.rect(Ac+640, Ar, Ac, 360);
        ctx.stroke();        
        //box4 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "red";
        ctx.lineWidth = "8";
        ctx.rect(0, Ar+360, 1280, 180);
        ctx.stroke();
        
        //set video position with canvas
        let canvasElem = document.querySelector('canvas');
        let canvasRect = canvasElem.getBoundingClientRect();
        this.setState({
            xoffset:canvasRect.left,
            yoffset:canvasRect.top,
            canLe:canvasRect.left,
            canTo:canvasRect.top,
            canWi:canvasRect.width,
            canHe:canvasRect.height
        })

        this.interval=setInterval(this.sendRequest,500);
    }
    componentWillUnmount() {
        // Clear the interval right before component unmount
        clearInterval(this.interval);
    }
    sendRequest = () => {
        if(
            typeof this.webcam !== "undefined" &&
            this.webcam !== null &&
            this.webcam.video.readyState === 4
          )
          {
            //base64 image
            var imageSrc=this.webcam.getScreenshot({width: 1280, height: 720});
            //remove "data:image/jpeg;base64,"
            imageSrc=imageSrc.replace('data:image/jpeg;base64,','');
            //send request            
            const fd=new FormData();
            fd.append('b64image',imageSrc)
            const url='http://localhost:8000/webcamFD/'
            let requestTimer=500;
            axios.post(url,fd)
            .then((response)=>{
                
                //update frame boxes
                if(typeof response.data.left!=="undefined" && typeof response.data.upper!=="undefined"){
                    //console.log("left-upper:::"+response.data.left+" | "+response.data.upper)
                    //console.log("right-lower:::"+response.data.right+" | "+response.data.lower)
                    //if B=(x,y) middle of blob and capture size mxn
                    var x=this.state.xoffset+(response.data.left+response.data.right)/4;
                    var y=(response.data.upper+response.data.lower)/2;
                    //canvas origin
                    var cnvX=this.state.canLe+this.state.canWi/2;
                    var cnvY=this.state.canTo+this.state.canHe/2;
                    //move               
                    const processTimer=10;
                    var step=0;
                    var range=0;
                    
                    if( x<cnvX-80 && 
                        this.state.xoffset<this.state.canLe+160
                        ){             
                        //console.log("kçük sağa git")         
                        range=(cnvX-x);
                        step=(cnvX-x)/(requestTimer/processTimer);
                        var process=setInterval(()=>{                            
                            if(range<0 || this.state.xoffset>this.state.canLe+140){ 
                               clearInterval(process);
                            }
                            this.setState({
                                xoffset:this.state.xoffset+step
                            })
                            range-=step
                        },processTimer);
                    }else if( x>cnvX+80 &&
                              this.state.xoffset>this.state.canLe-160
                            ){             
                            //console.log("büyük sola git")           
                            range=(x-cnvX);
                            step=(x-cnvX)/(requestTimer/processTimer);
                            var process=setInterval(()=>{                            
                                if(range<0 || this.state.xoffset<this.state.canLe-140){ 
                                clearInterval(process);
                                }
                                this.setState({
                                    xoffset:this.state.xoffset-step
                                })
                                range-=step
                            },processTimer);
                    }
                    
                    this.sleep(50).then(()=>{
                        if( y<cnvY-40 &&                        
                            this.state.yoffset<this.state.canTo+70
                            ){
                            range=(cnvY-y);
                            step=(cnvY-y)/(requestTimer/processTimer);
                            var process=setInterval(()=>{                            
                                if(range<0 || this.state.yoffset>this.state.canTo+70){ 
                                   clearInterval(process);
                                }
                                this.setState({
                                    yoffset:this.state.yoffset+step
                                })
                                range-=step
                            },processTimer);
                        }else if(
                                y>cnvY+40 &&                            
                                this.state.yoffset>this.state.canTo-70
                        ){
                            range=(y-cnvY);
                            step=(y-cnvY)/(requestTimer/processTimer);
                            var process=setInterval(()=>{                            
                                if(range<0 || this.state.yoffset<this.state.canTo-70){ 
                                   clearInterval(process);
                                }
                                this.setState({
                                    yoffset:this.state.yoffset-step
                                })
                                range-=step
                            },processTimer);
                        }
                    })
                    
                }    
            }).catch(err=>{
                console.log(err)
            })
          }
    }
    sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
    render() {
        const videoConstraints = {
            width: 1280,
            height: 720,
            facingMode: "user"
        };
      return(
        <div className="WebcamApp">
            <header className="App-header">
                <Webcam
                    audio={false}
                    height={360}
                    ref={this.webcamRef}
                    screenshotFormat="image/jpeg"
                    width={640}
                    videoConstraints={videoConstraints}
                    style={{
                        position: "absolute",
                        left: `${this.state.xoffset}px`,
                        top: `${this.state.yoffset}px`,
                    }}
                />
                <canvas
                    ref={this.canvasRef}
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
}

export default WebCamComp4;