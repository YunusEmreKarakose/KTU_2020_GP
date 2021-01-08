import React from 'react'
import FSChild from './formSelectorChild'
class FormSelector extends React.Component{
    constructor() {
        super()
        this.state = {
            isSelected:false,
            form1:false,
            form2:false,
            form3:false,
        }
        this.onClickHandler=this.onClickHandler.bind(this)
    }
    onClickHandler(event){
        if(this.state.isSelected){
            this.setState({
                form1:false,
                form2:false,
                form3:false,
                form4:false
            })
            this.setState({
                [event.target.name]:true
            })
            //console.log("render"+event.target.name)
        }else{
            this.setState({
                [event.target.name]:true,
                isSelected:true
            })            
            //console.log("render"+event.target.name)
        }
    }
    
    render() {
        return (
            <div>
                <div>
                    <button type="submit" name="form1" onClick={this.onClickHandler}>Form1</button>
                    <button type="submit" name="form2" onClick={this.onClickHandler}>Form2</button>
                    <button type="submit" name="form3" onClick={this.onClickHandler}>Form3</button>
                    <button type="submit" name="form4" onClick={this.onClickHandler}>Form4</button>
                </div>
                <FSChild 
                    form1={this.state.form1}
                    form2={this.state.form2}  
                    form3={this.state.form3}
                    form4={this.state.form4}
                />                  
            </div>
        )
    }

}

export default FormSelector