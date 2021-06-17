// Import dependencies
import React from "react";
import Webcam from "react-webcam";
import axios from 'axios'

class WebCamComp3 extends React.Component {
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
    moveTitleToDown = () => {
        this.setState(
            { yoffset: this.state.yoffset 
              + 20 });
    };
    moveTitleToRight = () => {
        this.setState(
            { xoffset: this.state.xoffset 
              + 20 });
    };
    moveTitleToLeft = () => {
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
        this.setState(
            { xoffset: this.state.xoffset 
              - 20 });
    };
    moveTitleToUp = () => {
        this.setState(
            { yoffset: this.state.yoffset 
              - this.state.delta });
    };
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
        ctx.strokeStyle = "#252c37";   
        ctx.lineWidth = "8";
        ctx.rect(0, 0, 1280, Ar);
        ctx.stroke();
        //box2 0,Ac,Ar,360    
        ctx.beginPath();
        ctx.strokeStyle = "#252c37";  
        ctx.lineWidth = "8";
        ctx.rect(0, Ar, Ac, 360);
        ctx.stroke();
        //box3 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "#252c37"; 
        ctx.lineWidth = "8";
        ctx.rect(Ac+640, Ar, Ac, 360);
        ctx.stroke();        
        //box4 Ar+640,Ac,640-Ar,Ac     
        ctx.beginPath();
        ctx.strokeStyle = "#252c37";
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

        this.interval=setInterval(this.sendRequest,3000);
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
            //mid point of canvas
            let cx=this.state.canLe+(this.state.canWi/2)
            let cy=this.state.canTo+(this.state.canHe/2)
            let requestTimer=3000;
            axios.post(url,fd)
            .then((response)=>{
                
                //update frame boxes
                if(typeof response.data.left!=="undefined" && typeof response.data.upper!=="undefined"){
                    //console.log("left-upper:::"+response.data.left+" | "+response.data.upper)
                    //console.log("right-lower:::"+response.data.right+" | "+response.data.lower)
                    //if B=(x,y) middle of blob and capture size mxn
                    var x=this.state.canLe+(response.data.left+response.data.right)/4;
                    var y=this.state.canTo+(response.data.upper+response.data.lower)/4;                    
                    const processTimer=50;
                    const step=(requestTimer/2)/processTimer;
                    // |x-cx|<320
                    
                    if ((x-cx)>0 && this.state.xoffset>this.state.canLe-140){
                        var limit=140
                        if (x-cx<60){
                            limit=x-cx
                        }
                        var process=setInterval(()=>{                            
                            if(this.state.xoffset<=this.state.canLe-limit){  
                               clearInterval(process);
                            }
                            this.setState({
                                xoffset:this.state.xoffset-step
                            })
                         },processTimer);
                    }else if((x-cx)<0 && this.state.xoffset<this.state.canLe+140){
                        var limit=140
                        if (x-cx>-60){
                            limit=cx-x
                        }
                        var process=setInterval(()=>{                            
                            if(this.state.xoffset>=this.state.canLe+limit){  
                               clearInterval(process);
                            }
                            this.setState({
                                xoffset:this.state.xoffset+step
                            })
                         },processTimer);
                    }
                    /*
                    if ((y-cy)>0 && this.state.yoffset>this.state.canTo-15){
                        var limit=15
                        if (y-cy<25){
                            limit=y-cy
                        }
                        var process=setInterval(()=>{                            
                            if(this.state.yoffset<=this.state.canTo-limit){  
                            clearInterval(process);
                            }
                            this.setState({
                                yoffset:this.state.yoffset-step
                            })
                        },processTimer);
                    }else if((y-cy)<0 && this.state.yoffset<this.state.canTo+15){
                        var limit=15
                        
                        if (y-cy>-25){
                            limit=cy-y
                        }
                        var process=setInterval(()=>{                            
                            if(this.state.yoffset>=this.state.canTo+limit){  
                            clearInterval(process);
                            }
                            this.setState({
                                yoffset:this.state.yoffset+step
                            })
                        },processTimer);
                    }
                    /*
                    this.sleep(100).then(()=>{
                        
                        //|y-cy|<180
                        if ((y-cy)>0 && this.state.yoffset>this.state.canTo-60){
                            var limit=60
                            if (y-cy<25){
                                limit=y-cy
                            }
                            var process=setInterval(()=>{                            
                                if(this.state.yoffset<=this.state.canTo-limit){  
                                clearInterval(process);
                                }
                                this.setState({
                                    yoffset:this.state.yoffset-step
                                })
                            },processTimer);
                        }else if((y-cy)<0 && this.state.yoffset<this.state.canTo+60){
                            var limit=60
                            
                            if (y-cy>-25){
                                limit=cy-y
                            }
                            var process=setInterval(()=>{                            
                                if(this.state.yoffset>=this.state.canTo+limit){  
                                clearInterval(process);
                                }
                                this.setState({
                                    yoffset:this.state.yoffset+step
                                })
                            },processTimer);
                        }
                    })
                    */
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
                <div style={{ marginTop: "500px" }}>
                    <button onClick={this.moveTitleToRight}>
                        Move Title To Right
                    </button>
                    <button onClick={this.moveTitleToDown}>
                        Move Title To Down
                    </button>
                    <button onClick={this.moveTitleToLeft}>
                        Move Title To Left
                    </button>
                    <button onClick={this.moveTitleToUp}>
                        Move Title To Up
                    </button>
                </div>
            </header>
        </div>
      );
    }
}

export default WebCamComp3;