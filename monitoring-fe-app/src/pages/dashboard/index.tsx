import Header from "../../components/header";
import "./dashboardStyle.scss";
import { useNavigate } from "react-router-dom";


import { Pie } from '@ant-design/plots';
interface DataType {
  type: string;
  value: number;
}

const DemoPie = () => {

  const colors: Record<string, string>  = {
    "Low battery": 'red',
    "In Charge": 'blue',
    "Above 50%": 'green',
  };

  const config = {
    data: [
      { type: "Above50%", value: 10 },
      { type: "Low battery", value: 50 },
      { type: "In Charge", value: 40 },
      { type: "In Charge", value: 40 },
      { type: "In Charge", value: 40 },
      { type: "In Charge", value: 40 },
    ] as DataType[] ,
    // color: (type:string) => colors[type],
    color: ['type', (type:string) => colors[type]],

    angleField: 'value',
    colorField: 'type',
    paddingRight: 100,
    innerRadius: 0.7,
    // radius: 0.8,
    label: {
      text: 'value',
      style: {
        fontWeight: 'bold',
      },
    },
    legend: {
      color: {
        // title: false,
        position: 'right',
        rowPadding: 5,
      },
    },
    annotations: [
      {
        type: 'text',
        style: {
          text: '20',
          x: '50%',
          y: '50%',
          textAlign: 'center',
          fontSize: 18,
          fontStyle: 'bold',
        },
      },
    ],
  };
  return <Pie {...config} />;
};



const Dashboard = () => {
  const navigate = useNavigate();

  const cards=()=>{
    return <div className="count-card" onClick={() => {}}>
    <div className="label-style">Total : Device</div>
    <div className="count-text">12</div>
  </div>
  }
  return (
    <div className="dashboard-container">
      <Header />
      <div className="dashboard-body">
        <div className="dashboard-top-count-cards">
          {cards()}
          {cards()}
          {cards()}
          {cards()}
          {cards()}
        </div>

        <div className="dashboard-chart-details">
          <div className="battery-status-card">
            <DemoPie/>
          </div>
          <div className="battery-status-card">

          </div>

          <div className="battery-status-card">

          </div>
        </div>
        
      </div>
    </div>
  );
};
export default Dashboard;
