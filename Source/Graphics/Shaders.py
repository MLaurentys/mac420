from PyQt5.QtCore import QObject
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram

## singleton shader class 
class Shaders(QObject):

    __instance = None

    def __new__(cls):
        if Shaders.__instance is None:
            Shaders.__instance = QObject.__new__(cls)
            Shaders.__instance.initialize()
        return Shaders.__instance


    def initialize(self):
        """Create shader programs"""

        ## create tessalation shader to subdivide icosahedron
        self.__instance._subdivTessalationShader = QOpenGLShaderProgram()
        self.__instance._subdivTessalationShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.sivs())
        self.__instance._subdivTessalationShader.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.SphereIcosControlShader())
        self.__instance._subdivTessalationShader.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.sites())
        self.__instance._subdivTessalationShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.sifs())
        self.__instance._subdivTessalationShader.link()

        ## create tessalation shader to subdivide icosahedron WITHOUT LIGHT
        self.__instance._subdivTessalationShaderNoLight = QOpenGLShaderProgram()
        self.__instance._subdivTessalationShaderNoLight.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.sivs())
        self.__instance._subdivTessalationShaderNoLight.addShaderFromSourceCode(QOpenGLShader.TessellationControl, Shaders.SphereIcosControlShader())
        self.__instance._subdivTessalationShaderNoLight.addShaderFromSourceCode(QOpenGLShader.TessellationEvaluation, Shaders.sitesnl())
        self.__instance._subdivTessalationShaderNoLight.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.sifsnl())
        self.__instance._subdivTessalationShaderNoLight.link()


        ## create background shader program
        self.__instance._backgroundShader = QOpenGLShaderProgram()
        self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorNoTransformVertexShader())
        self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._backgroundShader.link()

        ## create uniform material shader with no lighting 
        self.__instance._wireframeMaterialShader = QOpenGLShaderProgram()
        self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.wireframeMaterialVertexShader())
        self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._wireframeMaterialShader.link()

        ## create uniform material shader with no lighting 
        self.__instance._uniformMaterialShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialVertexShader())
        self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._uniformMaterialShader.link()

        ## create uniform material with no lighting calculations
        self.__instance._attributeColorShader = QOpenGLShaderProgram()
        self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTransformVertexShader())
        self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._attributeColorShader.link()

        ## create Phong mesh shader
        self.__instance._uniformMaterialPhongShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexShader())
        self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentShader())
        self.__instance._uniformMaterialPhongShader.link()

        ## create color-based Phong mesh shader
        self.__instance._attributeColorPhongShader = QOpenGLShaderProgram()
        self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexShader())
        self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentShader())
        self.__instance._attributeColorPhongShader.link()

        ## create Phong mesh shader
        self.__instance._uniformMaterialPhongFlatShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexFlatShader())
        self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentFlatShader())
        self.__instance._uniformMaterialPhongFlatShader.link()

        ## create color-based Phong mesh shader
        self.__instance._attributeColorPhongFlatShader = QOpenGLShaderProgram()
        self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexFlatShader())
        self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentFlatShader())
        self.__instance._attributeColorPhongFlatShader.link()

        ## create simple textured-based mesh shader
        self.__instance._texturedShader = QOpenGLShaderProgram()
        self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexShader())
        self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentShader())
        self.__instance._texturedShader.link()    

        ## create simple textured-based mesh flat shader
        self.__instance._texturedFlatShader = QOpenGLShaderProgram()
        self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexFlatShader())
        self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentFlatShader())
        self.__instance._texturedFlatShader.link()    

        self.__instance._normalVisShader = QOpenGLShaderProgram()
        self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.normalVisVertexShader())
        self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Geometry, Shaders.normalVisGeometryShader())
        self.__instance._normalVisShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.normalVisFragmentShader())
        self.__instance._normalVisShader.link()


    @classmethod
    def sivs(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        
        smooth out vec3 vPosition;
        smooth out vec3 vNormal;

        void main() {
            vPosition = position;
            vNormal = normal;
        }
        """
        return vertexShaderSource

    @classmethod
    def SphereIcosControlShader(cls):
        controlTessalationShaderSource = (
        '''
		#version 400 core
		layout(vertices = 3) out;
		
		smooth in vec3 vPosition[];
        smooth in vec3 vNormal[];

		uniform int innerSubdivisionLevel;
		uniform int outerSubdivisionLevel;

		out vec3 tcPosition[];
		out vec3 tcNormal[];

		void main()
		{
			tcPosition[gl_InvocationID] = vPosition[gl_InvocationID];
            tcNormal[gl_InvocationID] = vNormal[gl_InvocationID];
			gl_TessLevelInner[0] = innerSubdivisionLevel;
			gl_TessLevelOuter[0] = outerSubdivisionLevel;
			gl_TessLevelOuter[1] = outerSubdivisionLevel;
			gl_TessLevelOuter[2] = outerSubdivisionLevel;
		}
		'''
        )
        return controlTessalationShaderSource

    @classmethod
    def sites(cls):
        evalShader = (
            """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

		in vec3 tcPosition[];
        in vec3 tcNormal[];

        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;
        uniform float radius;

        out vec3 tePatchDistance;
        out vec4 tePosition;
        out vec4 teNormal;
        smooth out vec3 lightDirection;
        smooth out float attenuation;

		void main()
		{
            //vertices positions
			vec3 p0 = gl_TessCoord.x * tcPosition[0];
			vec3 p1 = gl_TessCoord.y * tcPosition[1];
			vec3 p2 = gl_TessCoord.z * tcPosition[2];
            vec3 pos = radius * vec3(normalize(p0 + p1 + p2));

            //normal values
			vec3 n0 = gl_TessCoord.x * tcNormal[0];
			vec3 n1 = gl_TessCoord.y * tcNormal[1];
			vec3 n2 = gl_TessCoord.z * tcNormal[2];
            vec3 normal = vec3(normalize(n0 + n1 + n2));

            //light values
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            }
            else {
                lightDirection = normalize(lightPosition.xyz - tePosition.xyz);
                float distance = length(lightPosition.xyz - tePosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }

            //gl values
            tePosition = viewMatrix * modelMatrix * vec4(pos, 1.0);
            teNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            tePatchDistance = gl_TessCoord;
			gl_Position = projectionMatrix * tePosition;
		}
		"""
        )
        return evalShader

    @classmethod
    def sifs(cls):
        fragmentShaderSource = (
        """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        out vec3 tePatchDistance;
        in vec4 tePosition;
        in vec4 teNormal;
        smooth in vec3 lightDirection;
        smooth in float attenuation;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {

            //vec3 color = vec3(0.0, 0.5, 0.0);
            //FragColor = vec4(color, 1.0);

            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(teNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-tePosition.xyz);
            vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }

        """)
        return fragmentShaderSource

    @classmethod
    def sitesnl(cls):
        evalShader = (
            """
		#version 400 core
		layout(triangles, equal_spacing, ccw) in;

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

		in vec3 tcPosition[];
        in vec3 tcNormal[];

        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform float radius;
        uniform Material material;
        out vec4 tePosition;
        out vec4 teColor;

		void main()
		{
           //vertices positions
			vec3 p0 = gl_TessCoord.x * tcPosition[0];
			vec3 p1 = gl_TessCoord.y * tcPosition[1];
			vec3 p2 = gl_TessCoord.z * tcPosition[2];
            vec3 pos = radius * vec3(normalize(p0 + p1 + p2));

            teColor = vec4(material.diffuse, 1.0);

            //gl values
            tePosition = viewMatrix * modelMatrix * vec4(pos, 1.0);
			gl_Position = projectionMatrix * tePosition;
		}
		"""
        )
        return evalShader

    @classmethod
    def sifsnl(cls):
        fragmentShaderSource = (
        """
        #version 400

        in vec4 teColor;
        in vec4 tePosition;

        out vec4 fragColor;

        void main()
        {

            fragColor = teColor;
        }

        """)
        return fragmentShaderSource

    @classmethod
    def uniformMaterialPhongVertexFlatShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialPhongFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeMaterialPhongVertexFlatShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 vertexColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            vertexColor = color;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeMaterialPhongFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 vertexColor;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource
        

    @classmethod
    def uniformMaterialPhongVertexShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialPhongFragmentShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeMaterialPhongVertexShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 vertexColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            vertexColor = color;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeMaterialPhongFragmentShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 vertexColor;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeColorNoTransformVertexShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 2) in vec3 color;
        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = vec4(position, 1.0);
            vertexColor = vec4(color, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialVertexShader(cls):
        vertexShaderSource = """
        #version 400
        
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        layout(location = 0) in vec3 position;
        
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform Material material;

        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(material.diffuse, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def texturedVertexShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        layout(location = 3) in vec2 texcoord;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec2 textureCoord;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            textureCoord = texcoord;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def texturedVertexFlatShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        layout(location = 3) in vec2 texcoord;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec2 textureCoord;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            textureCoord = texcoord;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def wireframeMaterialVertexShader(cls):
        vertexShaderSource = """
        #version 400
        
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        layout(location = 0) in vec3 position;
        
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform Material wireframe_material;

        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(wireframe_material.diffuse, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeColorTransformVertexShader(cls):
        vertexShaderSource = """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(color, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def simpleFragmentShader(cls):
        fragmentShaderSource = """
        #version 400
        smooth in vec4 vertexColor;
        out vec4 fragColor;

        void main()
        {
            fragColor = vertexColor;
        }
        """
        return fragmentShaderSource


    @classmethod
    def texturedFragmentShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec2 textureCoord;

        uniform float selected;
        uniform sampler2D texObject;
        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            vec4 tex = texture(texObject, textureCoord.st);
            fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def texturedFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 400
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;    
            float shininess;
        }; 

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec2 textureCoord;

        uniform float selected;
        uniform sampler2D texObject;
        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
             vec3 R = normalize(-reflect(L, N)); 
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            vec4 tex = texture(texObject, textureCoord.st);
            fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
        }
        """
        return fragmentShaderSource

    @classmethod
    def normalVisVertexShader(cls):
        return """
        #version 400
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;

        out vec3 vertexNormal;
        out vec3 vertexPosition;

        void main() 
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexPosition = position;
            vertexNormal = normal;
        }
        """

    @classmethod
    def normalVisGeometryShader(cls):
        return """
        #version 400
        layout(triangles) in;
        layout(line_strip, max_vertices = 4) out;

        in vec3 vertexNormal[];
        in vec3 vertexPosition[];

        const float a = 0.33;
        const float b = 0.33;
        const float c = 0.33;

        const float MAGNITUDE = 0.4;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;

        void main()
        {
            vec3 p0 = a*vertexPosition[0];
            vec3 p1 = b*vertexPosition[1];
            vec3 p2 = c*vertexPosition[2];
            vec3 p = p0 + p1 + p2;

            vec3 n0 = a * normalize(vertexNormal[0]);
            vec3 n1 = b * normalize(vertexNormal[1]);
            vec3 n2 = c * normalize(vertexNormal[2]);
            vec3 n = n0 + n1 + n2;

            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p, 1.0);
            EmitVertex();
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(p+n*MAGNITUDE, 1.0);
            EmitVertex();
            EndPrimitive();
        }"""

    @classmethod
    def normalVisFragmentShader(cls):
        return """
        #version 400
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }"""

    def backgroundShader(self):
        return self.__instance._backgroundShader

    def uniformMaterialShader(self):
        return self.__instance._uniformMaterialShader

    def wireframeMaterialShader(self):
        return self.__instance._wireframeMaterialShader

    def attributeColorShader(self):
        return self.__instance._attributeColorShader
        
    def uniformMaterialPhongShader(self):
        return self.__instance._uniformMaterialPhongShader

    def attributeColorPhongShader(self):
        return self.__instance._attributeColorPhongShader

    def uniformMaterialPhongFlatShader(self):
        return self.__instance._uniformMaterialPhongFlatShader

    def subdivTessalationShader(self):
        return self.__instance._subdivTessalationShader

    def subdivTessalationShaderNoLight(self):
        return self.__instance._subdivTessalationShaderNoLight

    def attributeColorPhongFlatShader(self):
        return self.__instance._attributeColorPhongFlatShader
        
    def texturedShader(self):
        return self.__instance._texturedShader

    def texturedFlatShader(self):
        return self.__instance._texturedFlatShader

    def normalVisShader(self):
        return self.__instance._normalVisShader
