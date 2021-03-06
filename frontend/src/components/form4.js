import React from 'react'
import axios from 'axios'
import ImageContainer from './imageContainer'
//MY FACE DETECTİON
class Form4 extends React.Component {
    constructor() {
        super()
        this.state = {
            image:null,
            proccesed:null,
            isLoad:false
        }
        //this.fileSelectedHandler=this.fileSelectedHandler.bind(this)
        this.handleChange=this.handleChange.bind(this)
    }
    handleChange(event){
        if(event.target.type==="text"){
            this.setState({
                [event.target.name]:event.target.value
            })
        }else if(event.target.type==="file"){            
            this.setState({
                [event.target.name]:event.target.files[0]
            })
        }              
    }
    submitHandler=(e)=>{
        e.preventDefault();
        const fd=new FormData();
        fd.append('image',this.state.image)
        const url='http://localhost:8000/myFaceDetection/'
        //setstate for loading
        this.setState({
            isLoad:true
        })
        axios.post(url,fd)
            .then((response)=>{
                //console.log(response)
                this.setState({
                    proccesed:response.data
                })
            }).catch(err=>{
                console.log(err)
            })
    }    
    
    render() {
        return (
            <div class="form1">
                <form onSubmit={this.submitHandler} >
                    <input type="file" name="image" class="fileinput" onChange={this.handleChange}></input>
                    <button type="submit" class="submitButton">Submit</button>
                </form>
                
                <div>
                    <ImageContainer isLoad={this.state.isLoad} image={this.state.proccesed} />
                </div>
            </div>
        )
    }
}

export default Form4