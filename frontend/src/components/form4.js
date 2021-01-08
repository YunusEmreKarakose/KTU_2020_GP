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
        axios.post(url,fd)
            .then((response)=>{
                //console.log(response)
                this.setState({
                    proccesed:response.data,
                    isLoad:true
                })
            }).catch(err=>{
                console.log(err)
            })
    }    
    
    render() {
        return (
            <div>
                <form onSubmit={this.submitHandler} class="form1">
                    <input type="file" name="image" onChange={this.handleChange}></input>
                    <button type="submit">Submit</button>
                </form>
                <div>
                    <ImageContainer isLoad={this.state.isLoad} image={this.state.proccesed} />
                </div>
            </div>
        )
    }
}

export default Form4