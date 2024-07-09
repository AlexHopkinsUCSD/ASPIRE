from typing import List, Protocol, Literal, Union

from app.domain.models.concept import (
    ConceptCreate, 
    ConceptRead, 
    ConceptToDomainCreate, 
    ConceptToDomainRead, 
    ConceptCreateBulkRead, 
    ConceptToModuleCreate, 
    ConceptToModuleRead,
    ConceptToConceptCreate,
    ConceptToConceptRead,
    ConceptFilter,
    ConceptBulkRead,
    ConceptReadVerbose,
    ConceptToModuleDelete,
    ConceptToConceptDelete
    )

class ConceptRepository(Protocol):
    async def add(self, concept: ConceptCreate) -> ConceptRead:
        """
        Adds a single concept to the db
        """
        ...

    async def bulk_add(self, concepts: List[ConceptCreate]) -> ConceptCreateBulkRead:
        """
        Adds many concepts to the db
        """
        ...

    async def get_one(self, concept_name: str, read_mode: Literal["normal", "verbose"] = "normal") -> Union[ConceptRead, ConceptReadVerbose]:
        """
        Returns a single concept filtered by name, 
        use read_mode='normal' for checking if a concept exists in the db,
        use read_mode='verbose' to return the details of a concept.

        :param concept_name: the name of the concept as a string
        :param read_mode: ('normal', 'verbose') in 'normal' mode just returns the concept name (useful to check if the concept exists in the db), in 'verbose' mode returns all the details of the concept
        """
        ...

    async def get_many(self, filters: ConceptFilter, domain_init_mode: bool=False, read_mode: Literal["normal", "verbose"] = "normal") -> Union[ConceptBulkRead, List[ConceptReadVerbose]]:
        """
        Returns all concepts matching a set of filters.
        :param filters: ConceptFilter(course_id: Optional[int], subject: Optional[str], difficulty: Optional[int]) - specifies which params to filter concepts by.
        :param read_mode: ('normal', 'verbose') in 'normal' mode returns only the concept name for each matching concept, in 'verbose' mode returns all the details of each matching concept
        """
        ...


class ConceptToDomainRepository(Protocol):
    async def add(self, junction: ConceptToDomainCreate) -> ConceptToDomainRead:
        """
        Creates a new ConceptToDomain Junction
        """
        ...

    async def bulk_add(self, junctions: List[ConceptToDomainCreate]) -> List[ConceptToDomainRead]:
        """
        Creates many new ConceptToDomain Junctions
        """
        ...

    async def get_all(self, domain_id: int) -> ConceptBulkRead:
        """
        Returns all concepts contained inside a domain
        """
        ...


class ConceptToModuleRepository(Protocol):
    async def add(self, junction: ConceptToModuleCreate) -> ConceptToModuleRead:
        """
        Creates one ConceptToModule junction
        """        
        ...

    async def bulk_add(self, junctions: List[ConceptToModuleCreate]) -> List[ConceptToModuleRead]:
        """
        Creates many ConceptToModule junctions
        """
        ...

    async def get_all(self, module_id: int) -> ConceptBulkRead:
        """
        Returns all concepts inside a module
        """
        ...

    async def delete(self, junctions: List[ConceptToModuleDelete]):
        """
        Removes a concept from a module
        """       
        ...

class ConceptToConceptRepository(Protocol):
    async def add(self, junction: ConceptToConceptCreate) -> ConceptToConceptRead:
        """
        Adds a single ConceptToConcept junction
        """
        ...

    async def bulk_add(self, junctions: List[ConceptToConceptCreate]) -> List[ConceptToConceptRead]:
        """
        Adds many ConceptToConcept junctions
        """
        ...

    async def get_some(
            self, 
            concepts: ConceptBulkRead, 
            junction_direction: Literal["up", "down", "both"]="down"
    ) -> List[ConceptToConceptRead]:
        """
        Returns the concept-to-concept relationships of specified concepts based on a specified junction_direction

        :param concepts: A ConceptBulkRead object containing a list of ConceptReads, used to filter which concepts to return the relationships of.
    
        :param junction_direction: ('up', 'down', 'both') The orientation of the relationship. 'up' returns all concepts dependent on the supplied concept, 'down' returns the prerequisites of the supplied concept, 'both' returns both.
    
        """
        ...

    async def delete(self, junctions: List[ConceptToConceptDelete]):
        """
        Deletes one or many ConceptToConcept junctions
        """
        ...