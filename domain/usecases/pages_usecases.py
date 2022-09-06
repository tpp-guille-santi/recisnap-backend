from odmantic import ObjectId, AIOEngine

from domain.entities import Page, PageUpdate, PageSearch
from domain.errors import PageNotFoundException
from infrastructure.repositories import GeorefRepository


class PagesUseCases:

    def __init__(self, engine: AIOEngine, georef_repository: GeorefRepository):
        self.engine = engine
        self.georef_repository = georef_repository

    async def create_page(self, page: Page) -> Page:
        page = await self.engine.save(page)
        return page

    async def list_pages(self) -> list[Page]:
        return await self.engine.find(Page)

    async def search_pages(self, search: PageSearch) -> list[Page]:
        query_filters = await self._generate_query_filters(search)
        return await self.engine.find(Page, *query_filters)

    async def _generate_query_filters(self, search: PageSearch) -> list[bool]:
        query_filters = []
        if search.latitude and search.longitude:
            georef_location = await self.georef_repository.get_georef_location(search.latitude,
                                                                               search.longitude)
            query_filters.append(Page.provincia == georef_location.ubicacion.provincia.nombre)
            query_filters.append(Page.municipio == georef_location.ubicacion.municipio.nombre)
            query_filters.append(Page.departamento == georef_location.ubicacion.departamento.nombre)
            return query_filters
        if search.material_name:
            query_filters.append(Page.material_name == search.material_name)
        if search.provincia:
            query_filters.append(Page.provincia == search.provincia)
        if search.municipio:
            query_filters.append(Page.municipio == search.municipio)
        if search.departamento:
            query_filters.append(Page.departamento == search.departamento)
        return query_filters

    async def get_page_by_id(self, id: ObjectId) -> Page:
        page = await self.engine.find_one(Page, Page.id == id)
        if not page:
            raise PageNotFoundException(id)
        return page

    # async def get_page_by_georef(self, id: ObjectId, app_page_request: AppPageRequest) -> Page:
    #     georef_location = await self.georef_repository.get_georef_location(app_page_request)
    #     page = await self.engine.find_one(
    #         Page,
    #         (Page.departamento == georef_location.ubicacion.departamento.nombre) &
    #         (Page.municipio == georef_location.ubicacion.municipio.nombre) &
    #         (Page.provincia == georef_location.ubicacion.provincia.nombre))
    #     if not page:
    #         raise PageNotFoundException(id)
    #     return page

    # async def get_pages_by_lat_long(self, id: ObjectId, app_page_request: AppPageRequest) -> Page:
    #     georef_location = await self.georef_repository.get_georef_location(app_page_request)
    #     page = await self.engine.find_one(
    #         Page,
    #         (Page.departamento.id == georef_location.ubicacion.departamento.id) &
    #         (Page.municipio.id == georef_location.ubicacion.municipio.id) &
    #         (Page.provincia.id == georef_location.ubicacion.provincia.id))
    #     if not page:
    #         raise PageNotFoundException(id)
    #     return page

    async def update_page_by_id(self, id: ObjectId, patch: PageUpdate) -> Page:
        page = await self.engine.find_one(Page, Page.id == id)
        if page is None:
            raise PageNotFoundException(id)
        page.update(patch)
        await self.engine.save(page)
        return page

    async def delete_page_by_id(self, id: ObjectId) -> Page:
        page = await self.engine.find_one(Page, Page.id == id)
        if page is None:
            raise PageNotFoundException(id)
        await self.engine.delete(page)
        return page
