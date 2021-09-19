import { Input, Button, Form, Layout, Menu, message, Divider, Row, Col, Select, Card } from 'antd';
import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import "antd/dist/antd.css";
import './App.css';

import {
  FileSearchOutlined, FormOutlined, RadarChartOutlined, LogoutOutlined, BankOutlined, DownOutlined, CaretRightFilled, DoubleLeftOutlined, EditOutlined, DeleteOutlined
} from '@ant-design/icons';

import { ForceGraph2D } from 'react-force-graph';
import {contentLongEnough} from './utils/utils.js'

require('dotenv/config');

const { TextArea } = Input;
const { Header, Content, Footer, Sider } = Layout;
const { Option } = Select;
const layout = {
  labelCol: {
    span: 3,
  },
  wrapperCol: {
    span: 16,
  }
};
const tailLayout = {
  wrapperCol: { offset: 3, span: 16 },
};

// const BASE_API_URI = 'http://127.0.0.1:5000/'
const BASE_API_URI = 'https://nodability-backend.herokuapp.com/'

let topics = ['cats', 'dogs','chess','fruit loops']

function App() {
  const [form] = Form.useForm();
  const [collapsed, setCollapsed] = useState(false);
  const [selectedPage, setSelectedPage] = useState('Write');
  const [selectedHomeLoginRegister, setSelectedHomeLoginRegister] = useState('Home');
  const [loggedIn, setLoggedIn] = useState(false);
  const [allTopics, setAllTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [committedTopic, setCommittedTopic] = useState('');
  const [selectedDocument, setSelectedDocument] = useState(
    {title: '', content: '', date: '', predictions: {keywords: '', topics: '', summary: ''}}
  );
  const [graphData, setGraphData] = useState({
    "nodes": [],
    "links": []
  });
  const [topicGraphData, setTopicGraphData] = useState({
    "nodes": [],
    "links": []
  });
  const onFinish = (values) => {
    if (!contentLongEnough(values["content"], 30)) {
      message.error({content: "Content must be 30 or more words!", duration: 3});
    } else {
      const req = {
        ...values
      }
  
      console.log(`Sending upload request to flask backend ...`);
      axios.post(BASE_API_URI+'upload', req)
        .then(res => {
          console.log(res);
          form.resetFields();
          if (res.data['message'] === "success") {
            message.success({content: "Content uploaded!", duration: 2});
          }
        })
        .catch(err => {
          console.log(err)
        })
      
      console.log("Trying to update topic data...")
      axios.post(BASE_API_URI+'pull_all_topics', req)
        .then(res => {
          console.log("Topic data updated")
          console.log(res);
          setAllTopics(() => res['data']['topics'])
        })
        .catch(err => {
          console.log(err)
          message.error({content: 'couldnt get db topic data!'})
        })
    }
  }
  const onFinishFailed = (errorinfo) => {
    console.log('Failed:', errorinfo)
  }
  const onReset = () => {
    form.resetFields();
  }
  const onRegister = (values) => {
    const req = {
      ...values
    }

    console.log(`Sending register request to flask backend ...`);
    const REGISTER_URI = 'http://127.0.0.1:5000/register'
    axios.post(REGISTER_URI, req)
      .then(res => {
        console.log(res);
        form.resetFields();
        if (res.data['message'] === 'success') {
          message.success({content: "Registered!", duration: 2});
          // redirect to write page (and "log in")
          setLoggedIn((loggedIn) => !loggedIn);
          console.log(loggedIn)
        }
      })
      .catch(err => {
        console.log(err)
      })
  }
  const onLogin = (values) => {
    console.log(values);

    console.log('attempting to login');
    const req = {
      ...values
    }

    if (values["email"] === "elon@musk.com" && values["password"] === "doge") {
      message.success({content: "Logged in", duration: 2});
      // redirect to write page
      setLoggedIn((loggedIn) => !loggedIn);
    } else {
      message.error({content: "to the moon?", duration: 2});
    }
    // console.log(req);
    // axios.post(BASE_API_URI+'login', req)
    //   .then(res => {
    //     if(res.status === 200) {
    //       message.success({content: "Logged in", duration: 2});
    //       // redirect to write page
    //       setLoggedIn((loggedIn) => !loggedIn);
    //     }
    //   })
    //   .catch(err => {
    //     console.log(err);
    //     message.error({content: "Log in failed!", duration: 2});
    //   })
}
  const handleNodeClick = (node) => {
    axios.post(BASE_API_URI+'pull_document', {id: node.id})
      .then(res => {
        console.log(res);
        setSelectedPage(()  => 'SpecificDocument')
        setSelectedDocument(() => res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
  const handleTopicQuery = () => {
    if(selectedTopic === '') {
      message.info("Select a topic first");
    } else if (selectedTopic === committedTopic) {
      console.log(`topic ${selectedTopic} already displayed`);
    } else {

      axios.post(BASE_API_URI+"pull_topic", {topic: selectedTopic})
        .then(res => {
          console.log(`pulled topic ${selectedTopic} data`)
          setCommittedTopic(() => selectedTopic);
          setTopicGraphData(res.data);
        })
    }
  }
  const HomeLoginRegisterComponents = {
    Home: (
      <div>
        <ForceGraph2D 
        graphData={graphData} 
        nodeAutoColorBy={() => Math.floor(Math.random()*20)}
        linkWidth={() => 6}
      />
      </div>
    ),
    Login: (
      <div>
        <Form
          { ...layout }
          onFinish={onLogin}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: 'Please input your email!' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password />
          </Form.Item>
    
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
            <Button type="text"
              onClick={() => message.info({
                content: "Username: elon@musk.com  Pass: doge",
                duration: 3
              })}>
              hint...
            </Button>
          </Form.Item>
        </Form>
        
      </div>
      
    ),
    Register: (
      <Form
        { ...layout }
        onFinish={onRegister}
        onFinishFailed={onFinishFailed}
      >
        <Form.Item
          label="Name"
          name="name"
          rules={[{ required: true, message: 'Please input your name!' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, message: 'Please input your email!' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Password"
          name="password"
          rules={[{ required: true, message: 'Please input your password!' }]}
        >
          <Input.Password />
        </Form.Item>
  
        <Form.Item
          label="Confirm Password"
          name="confirm"
          rules={[
            {
              required: true,
              message: 'Please confirm your password!',
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve();
                }
  
                return Promise.reject(new Error('The two passwords that you entered do not match!'));
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item>
  
        <Form.Item {...tailLayout}>
          <Button type="primary" htmlType="submit" disabled>
            Submit
          </Button>
        </Form.Item>
      </Form>
    )
  }
  const contentComponents = {
    Write: 
    (
      <div style={{padding: 18}}>
        <Divider orientation="center">Notepad</Divider>
        <Form { ...layout } onFinish={onFinish} form={form} onFinishFailed={onFinishFailed}>
          <Form.Item label="Title" name="title" rules={[{required: true, message: 'Enter a title!'}]}>
            <Input />
          </Form.Item>
          <Form.Item label="Content" name="content" id="article_content" rules={[{required: true, message: 'Write something!'}]}>
            <TextArea rows={8}/>
          </Form.Item>
          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit" style={{marginRight: 12}}>Submit</Button>
            <Button htmlType="button" onClick={onReset}>Clear</Button>
          </Form.Item>
        </Form>
      </div>
      
    ),
    Graph:
    (
      <div style={{padding: 18, height: '100%'}}>
        <Divider orientation="center">Nodability: <span style={{fontFamily: 'monospace'}}>{committedTopic}</span> Graph Representations</Divider>
        <Row>
          <Col flex={1}>
            <Select
            style={{ width: 220 }}
            showSearch
            placeholder="Select a topic"
            optionFilterProp="children"
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
            onChange={(value) => setSelectedTopic(value)}
            >
              {allTopics.map((topic) => {
                return (
                  <Option value={topic}>{topic}</Option>
                )
              })}
            </Select>
            <Button type="primary" onClick={handleTopicQuery}><CaretRightFilled/></Button>
          </Col>
          <Col flex={4} style={{height: '80%'}}>
          <ForceGraph2D 
            graphData={topicGraphData} 
            nodeAutoColorBy={() => Math.floor(Math.random()*20)} 
            onNodeClick={handleNodeClick}
            linkWidth={() => 6} 
          />
          </Col>
        </Row>
      </div>
    ),
    Search:
    (
      <div>working on search...</div>
    ),
    SpecificDocument:
    (
      <div style={{padding: 18, height: '100%'}}>
        <div style={{display: 'flex'}}>
          <Button type="primary" onClick={() => setSelectedPage("Graph")}><DoubleLeftOutlined /></Button>
          <div style={{marginLeft: 'auto', marginRight: 0}}>
            <Button type="default" disabled><EditOutlined style={{color: '#389e0d'}}/></Button>
            <Button type="default" disabled><DeleteOutlined style={{color: 'red'}}/></Button>
          </div>
        </div>
        
        <Divider orientation="center">{selectedDocument['title']}</Divider>
        <div>
          Created by: <i>{'elongated muskrat'}</i> on <i>{selectedDocument['date']}</i>
        </div>
        <Row gutter={16} style={{marginBottom: '14px'}}>
          <Col span={8}>
            <Card title="Keywords" bordered={false} style={{height: '28vh', overflow: 'auto'}}>
              {selectedDocument['predictions']['keywords'].replaceAll(",", ", ")}
            </Card>
          </Col>
          <Col span={8}>
            <Card title="Topics" bordered={false} style={{height: '28vh', overflow: 'auto'}}>
              {selectedDocument['predictions']['topics'].replaceAll(",", ", ")}
            </Card>
          </Col>
          <Col span={8}>
            <Card title="Summary" bordered={false} style={{height: '28vh', overflow: 'auto'}}>
              {selectedDocument['predictions']['summary']}
            </Card>
          </Col>
        </Row>
        <Card style={{width: '100%', height: '50vh', overflow: 'auto'}} title="Content">{selectedDocument['content']}</Card>
      </div>
    ),
    Logout: 
    (
      <div>logging out...</div>
    )
  }

  useEffect(() => {
    const req = {
      key: 123
    }

    console.log('Trying to get database data...');
    
    axios.post(BASE_API_URI+'pull_all', req)
      .then(res => {
        console.log("Database data loaded")
        console.log(res);
        setGraphData(res["data"]);
      })
      .catch(err => {
        console.log(err)
        message.error({content: 'couldnt get db data!'})
      })
    
    console.log("Trying to get topic data...")
    axios.post(BASE_API_URI+'pull_all_topics', req)
      .then(res => {
        console.log("Topic data loaded")
        console.log(res);
        setAllTopics(() => res['data']['topics'])
      })
      .catch(err => {
        console.log(err)
        message.error({content: 'couldnt get db topic data!'})
      })
  }, [])
  return (
    <div className="PageContent">
      {!loggedIn && (
        <Layout style={{height: '100vh'}}>
          <Header style={{background: "#5cdbd3"}}>
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%'}}>
              <Button type="text" className="logo" onClick={() => setSelectedHomeLoginRegister('Home')}> <BankOutlined /> NODABILITY</Button>
              <Button type="text" onClick={() => setSelectedHomeLoginRegister('Register')}>Register</Button>
              <Button type="text" onClick={() => setSelectedHomeLoginRegister('Login')}>Login</Button>
            </div>
          </Header>
          <Content>
            <div style={{height: '100%', background: '#fffbe6', padding: "18px 24px"}}>
              {HomeLoginRegisterComponents[selectedHomeLoginRegister]}
            </div>
          </Content>
        </Layout>
        
      )}
      {loggedIn && (
        <Layout style={{height: '100vh'}}>
          <Sider collapsible collapsed={collapsed} onCollapse={() => setCollapsed(() => !collapsed)}>
            <Menu theme="dark" selectedKeys={selectedPage} mode="inline" onSelect={(e) => setSelectedPage(e.key)}>
              <Menu.Item key="Write" icon={<FormOutlined />}>
                Write
              </Menu.Item>
              <Menu.Item key="Graph" icon={<RadarChartOutlined />}>
                Graph
              </Menu.Item>
              <Menu.Item key="Search" icon={<FileSearchOutlined />} disabled>
                Search
              </Menu.Item>
              <div className="logout" onClick={() => setLoggedIn((loggedIn) => !loggedIn)}>
                <LogoutOutlined style={{marginRight: 10}}/> logout
              </div>
            </Menu>
          </Sider>
          <Layout>
            <Content>
              {contentComponents[selectedPage]}
            </Content>
            <Footer style={{background: '#8c8c8c', textAlign: 'center', padding: '12px'}}>Bill Sun &copy; 2021</Footer>
          </Layout>
        </Layout>
      )}
      
    </div>
  );
}

export default App;