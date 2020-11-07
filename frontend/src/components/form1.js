import React from 'react'
import axios from 'axios'
import ImageContainer from './imageContainer'
//detect specific face and corrupt
class Form1 extends React.Component {
    constructor() {
        super()
        this.state = {
            image:null,
            targetImage:null,
            corruptFactor:null,
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
        fd.append('targetImage',this.state.targetImage)
        fd.append('corruptFactor',this.state.corruptFactor)
        const url='http://localhost:8000/detectSFaceAndCorrupt/'
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
                    <input type="file" name="targetImage" onChange={this.handleChange}></input>                    
                    <input type="text" name="corruptFactor" onChange={this.handleChange}></input>
                    <button type="submit">Submit</button>
                </form>
                <div>
                    <ImageContainer isLoad={this.state.isLoad} image={this.state.proccesed} />
                </div>
            </div>
        )
    }
}

export default Form1