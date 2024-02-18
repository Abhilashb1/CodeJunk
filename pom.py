import xml.dom.minidom

def parse_pom_for_dependencies(pom_path):
    dependencies = []
    
    # Parse the XML file
    dom_tree = xml.dom.minidom.parse(pom_path)
    
    # Get the root element
    root = dom_tree.documentElement
    
    # Get all properties
    properties = {}
    properties_elements = root.getElementsByTagName('properties')
    if properties_elements:
        for property_element in properties_elements[0].getElementsByTagName('*'):
            properties[property_element.tagName] = property_element.firstChild.nodeValue
    
    # Find all dependency elements
    dependency_elements = root.getElementsByTagName('dependency')
    
    for dependency_element in dependency_elements:
        # Get group ID
        group_id = dependency_element.getElementsByTagName('groupId')[0].firstChild.nodeValue
        
        # Get artifact ID
        artifact_id = dependency_element.getElementsByTagName('artifactId')[0].firstChild.nodeValue
        
        # Get version
        version_element = dependency_element.getElementsByTagName('version')
        if version_element:
            version_value = version_element[0].firstChild.nodeValue.strip()
            # Check if version contains a property reference
            if version_value.startswith('${') and version_value.endswith('}'):
                property_name = version_value[2:-1]  # Extract property name
                # Check if the property is defined
                if property_name in properties:
                    version = properties[property_name]
                else:
                    version = ''
            else:
                version = version_value
        else:
            # Handle case where version tag is not specified
            version = get_version_from_parent_pom(dependency_element, properties)
        
        dependencies.append((group_id, artifact_id, version))
    
    return dependencies

def get_version_from_parent_pom(dependency_element, properties):
    parent_element = dependency_element.parentNode
    while parent_element.tagName != 'project':
        parent_element = parent_element.parentNode
    
    # Check if parent POM is found
    if parent_element.tagName == 'project':
        # Look for version in parent POM
        parent_version = None
        for parent_dependency in parent_element.getElementsByTagName('dependency'):
            if parent_dependency.getElementsByTagName('groupId')[0].firstChild.nodeValue == dependency_element.getElementsByTagName('groupId')[0].firstChild.nodeValue and \
               parent_dependency.getElementsByTagName('artifactId')[0].firstChild.nodeValue == dependency_element.getElementsByTagName('artifactId')[0].firstChild.nodeValue:
                parent_version_element = parent_dependency.getElementsByTagName('version')
                if parent_version_element:
                    parent_version_value = parent_version_element[0].firstChild.nodeValue.strip()
                    if parent_version_value.startswith('${') and parent_version_value.endswith('}'):
                        property_name = parent_version_value[2:-1]
                        if property_name in properties:
                            parent_version = properties[property_name]
                        else:
                            parent_version = ''
                    else:
                        parent_version = parent_version_value
                break
    
        return parent_version
    
    return ''

# Example usage
pom_file_path = 'path/to/your/pom.xml'
dependencies = parse_pom_for_dependencies(pom_file_path)

for group_id, artifact_id, version in dependencies:
    print(f"Dependency: {group_id}:{artifact_id}, Version: {version}")
